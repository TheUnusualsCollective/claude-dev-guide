# RBF Pole Vector Prediction - Implementation Workflow

**Last Updated**: 2025-10-23

---

## Document Purpose

This document defines the specific approach for processing MOCAP data and implementing the RBF pole vector prediction system, from data ingestion through runtime evaluation.

---

## 1. Incoming Data Handling

### Data Sources & Format

Bandai: **BVH** format

1. D:\dev\projects\MOCAP\Bandai-Namco-Research-Motiondataset-master\dataset\Bandai-Namco-Research-Motiondataset-1

2. D:\dev\projects\MOCAP\Bandai-Namco-Research-Motiondataset-master\dataset\Bandai-Namco-Research-Motiondataset-2

### Loading Strategy

Initially we will load this data using python.

### Validation & Quality Checks

Make sure the nodes in the Joint Extraction section are present

Anything more is TBD until we see some results and/or find issues

---

## 2. Data Processing Pipeline

### Once Data is Loaded

We are interested in arms for now. This includes the clavicle (identified as "Shoulder" in the Bandai data set) to account for shoulder mobility.

In the Bandai data set the joints are identified as

- Shoulder_L, Shoulder_R

- UpperArm_L, UpperArm_R

- LowerArm_L, LowerArm_R

- Hand_L, Hand_R

### Joint Extraction

We are not actually "extracting" the joints, but we will need to perform some calculations to get the data we need. 

### Coordinate System & Transformations

**BVH Coordinate System:**
- Bandai BVH data loads correctly into Blender (Z-up)
- Native coordinate system uncertain (may already be Z-up, or Blender transforms on load)
- **Decision**: Defer coordinate system investigation until Maya testing

**Processing Strategy:**
- Use native BVH coordinate system for all calculations
- Apply axis transposition at the END (after all calculations)
- Simpler than transforming during processing

**Handedness (Left vs Right Arms):**
- **Store all data for ONE canonical side only** (choose right arm)
- Process left arm data by mirroring:
  - Multiply by -1 on transverse axis (X-axis typically)
  - Store `series_native_side` field to track original side
- At runtime, reverse the mirror if needed for left arm

**Result:** All training data represents right arm in consistent coordinate frame 

We will normalize our data using the total length of the arm as our normalizing divisor. This will allow us to store all of our data in a form that can easily be applied at runtime to characters of different sizes. 



#### Initialization Calculations

Calculate the length of the arm:

```C++
totalArmLength =
distance(Shoulder.worldPosition, ArmUpper.worldPosition) +
distance(ArmUpper.worldPosition, ArmLower.worldPosition) +
distance(ArmLower.worldPosition, Hand.worldPosition)
```

All positional values that we collect in the data gathering process will be divided by the `totalArmLength` value.



#### There are 2 primary output values that we are interested in:

Each of these values is collected for each frame of animation.

Each of these values is normalized based on the normalization notes above.

- **hand.worldPosition**
  
  - To calculate this is trivial

- **poleVector**

  - Algorithm:
    1. Project `LowerArm.worldPosition` onto the line from `UpperArm.worldPosition` to `Hand.worldPosition` → this gives `projectedPoint`
    2. Calculate direction vector: `direction = LowerArm.worldPosition - projectedPoint`
    3. Calculate pole vector: `poleVector = LowerArm.worldPosition + (direction * multiplier)`

  - Multiplier behavior:
    - `multiplier = 1.0`: poleVector is at the elbow (LowerArm.worldPosition)
    - `multiplier = 2.0`: poleVector is as far behind the elbow as projectedPoint was in front of it
    - **Default multiplier: TBD** (needs to be determined and stored in metadata) 



#### There are several other pieces of data that we are interested in:

Provided as single value

- series_name - basically the name of the animation

- gender

- characterization - this is a string identifier provided per animation in the Bandai data set. Unfortunately, it is not really categorically consistent in nature, so it may not be of use in the end.

- 

- 
  
  
  
  For example, here are the descriptors in data set 1:
  

For example:

These are from data set 1:

- normal
- happy
- sad
- angry
- proud
- not-confident
- masculinity
- feminine
- children
- old
- tired
- active
- musical
- giant
- chimpira



And these are from data set 2:    

- active
- elderly
- exhausted
- feminine
- masculine
- normal
- youthful



Calculated per frame (prefixed with `series_` if associated with the animation series):

- **series_frame** - Frame number within the animation sequence
  - Purpose: Track temporal sequence, useful for debugging and visualization
  - May not be used in model training initially

- **series_native_side** - Which side this data came from ("left" or "right")
  - Critical: All data stored for ONE canonical side only (mirroring applied during processing)
  - Data from opposite side is mirrored by multiplying by -1 on transverse axis

- **poleVector.velocity** (optional, future consideration)
  - Calculated as frame delta: `velocity[frame] = position[frame+1] - position[frame]`
  - Must be normalized by `totalArmLength`
  - Initially NOT used in model





### Data Cleaning & Filtering

This is TBD until we generate some output and have an idea what will be required based on the data set.

---

## 3. RBF Training Data Generation

**Important: Two-Stage Process**

This section describes the **second stage** - building RBF models from preprocessed data. Stage 1 (MOCAP → intermediate JSON) is described in Section 2.

### Intermediate File Format

Between MOCAP processing and model training, we generate **one JSON file per MOCAP file**.

**Rationale:**
- Separates geometric transforms from model iteration
- Allows fast iteration on model training without reprocessing MOCAP
- Easier debugging and data inspection
- One file per animation for easier investigation

**File Structure:**
```json
{
  "metadata": {
    "series_name": "animation_name",
    "series_gender": "male|female",
    "series_characterization": "normal|happy|...",
    "series_native_side": "right",
    "fps": 30,
    "total_frames": 120,
    "normalization_divisor": 2.45  // totalArmLength used for normalization
  },
  "frames": [
    {
      "series_frame": 0,
      "hand_position": [0.123, 0.456, 0.789],  // normalized
      "pole_vector": [0.234, 0.567, 0.890]     // normalized
    },
    // ... one entry per frame
  ]
}
```

### Feature Extraction (Input)

**Initial approach (simplest):**
- **Input to RBF**: `hand_position` (3D normalized coordinates)
  - Format: `[x, y, z]` where each value is normalized by `totalArmLength`

**Future considerations:**
- May add shoulder position, character metadata, velocity, etc.
- Starting simple to understand contribution of each feature

### Target Extraction (Output)

**RBF Output:**
- `pole_vector` (3D normalized coordinates)
  - Format: `[x, y, z]` where each value is normalized by `totalArmLength`

**Not initially included in output:**
- Velocity (may be added later as an input feature instead)

### Data Preparation

1. **Load all intermediate JSON files** from `data/processed/`
2. **Extract features**: Collect all `hand_position` values
3. **Extract targets**: Collect corresponding `pole_vector` values
4. **Flatten**: Each frame becomes one training sample
5. **Optional filtering**: By gender, characterization, etc. (TBD)

### Train/Test Split

- **Strategy**: TBD
- **Suggested**: 80/20 split, or hold out entire animations for testing
- **Consider**: Random split vs. animation-based split

---

## 4. RBF Model Training

### Kernel Selection

### Hyperparameters

### Training Process

### Validation

---

## 5. Model Export

### Export Format

### File Structure

### Metadata

---

## 6. Runtime Workflow (C++ Plugin)

### Initialization

### Per-Frame Evaluation

### Integration with Maya Rig

### Performance Considerations

---

## 7. End-to-End Example

### Example Scenario

---

## 8. Open Questions & Decisions Needed

### Processing Decisions

- **Pole vector multiplier value**: What constant to use? (1.5? 2.0? 3.0?)
  - Should this be tunable per-animation or constant?
  - Store in metadata for reproducibility

- **Which side to canonicalize to**: Right arm or left arm?
  - Recommendation: Right arm (more common convention)

- **Coordinate system**: Confirm BVH native coordinates and Maya target coordinates
  - Defer until Maya testing

### Model Training Decisions

- **Train/test split strategy**:
  - Random frame split?
  - Hold out entire animations?
  - Percentage split?

- **Kernel selection**: Which RBF kernel to use?
  - Test: gaussian, multiquadric, thin_plate_spline
  - Evaluate on validation set

- **Data filtering**: Should we filter by gender, characterization, etc.?
  - Or train one universal model?

### Data Quality

- **Number of animations to start**: 1 initially, then scale up
- **Visualization requirements**: Need 3D scatter plot widget (matplotlib with 3D axes?)
- **Quality metrics**: How to validate pole vector calculations are correct?






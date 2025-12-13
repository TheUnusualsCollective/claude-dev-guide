# Technology Stack

## Project: RBF Pole Vector Prediction

### Application Domain
**Character Animation Rigging** - Specifically IK (Inverse Kinematics) pole vector prediction

### Target Platforms
- **Maya** (Autodesk) - Primary target
- **Blender** (potentially, future consideration)

### Current Phase: R&D
**Architecture Decision Made**: Two-stage pipeline (Python training → C++ runtime)

---

## Architecture: Two-Stage Pipeline

### Stage 1: Model Training (Python)

**Language**: Python 3.8+

**Rationale**:
- Rich scientific computing ecosystem (NumPy, SciPy)
- Excellent for R&D and rapid prototyping
- Mature RBF implementations available
- Strong data analysis and visualization tools
- Fast iteration during research phase

**Purpose**:
- Develop and validate RBF approach
- Train models from MOCAP data
- Export trained models to file format

### Stage 2: Runtime Evaluation (C++)

**Language**: C++ (Maya API/SDK)

**Rationale**:
- **Real-time performance** - Must evaluate during playback
- **No Python dependency** - Eliminates version compatibility issues
- **Distribution** - Easier to deploy to other animators
- **Maya version independence** - Not tied to Maya's Python version
- **Optimization** - Can use SIMD, spatial indexing, etc.

**Purpose**:
- Load model files at runtime
- Evaluate RBF for pole vector predictions
- Integrate with Maya rig system

### Key Libraries (Candidates)

#### Scientific Computing
- **NumPy** - Array operations, linear algebra
- **SciPy** - RBF implementation (scipy.interpolate.RBFInterpolator)
- **scikit-learn** - Alternative ML-based approaches if needed

#### Data Handling
- *(TBD)* - For loading/processing MOCAP data
- Format depends on MOCAP data source (FBX, BVH, C3D, etc.)

#### Visualization (for R&D)
- **Matplotlib** - 2D/3D plotting for debugging and validation
- **Plotly** (optional) - Interactive 3D visualization

#### C++ Plugin Development (Future)
- **Maya C++ API** - For plugin development
- **Eigen** (optional) - Linear algebra library for C++
- **JSON library** (nlohmann/json or similar) - If using JSON model format
- **Performance libraries** - Potential SIMD/vectorization

---

## Model File Format (TBD)

The trained model needs to be serialized for the C++ plugin to load.

### Option 1: JSON (Human-Readable)
**Pros**: Easy to debug, inspect, version control
**Cons**: Larger file size, slower parsing
**Best for**: Development, small models

### Option 2: Binary (Compact)
**Pros**: Minimal file size, fast loading
**Cons**: Not human-readable, versioning harder
**Best for**: Production, large models

### Option 3: HDF5
**Pros**: Flexible, handles large arrays well, metadata support
**Cons**: Requires HDF5 library in C++
**Best for**: Very large models, complex metadata needs

### Model Contents:
```
{
  "version": "1.0",
  "kernel": "gaussian",
  "epsilon": 1.0,
  "centers": [[x1,y1,z1], [x2,y2,z2], ...],  // Nx3 array
  "weights": [[wx1,wy1,wz1], [wx2,wy2,wz2], ...],  // Nx3 array
  "normalization": {
    "input_mean": [x,y,z],
    "input_std": [x,y,z],
    "output_mean": [x,y,z],
    "output_std": [x,y,z]
  }
}
```

---

## RBF Training Approaches

### Approach 1: SciPy RBFInterpolator (Recommended for R&D)
- Use `scipy.interpolate.RBFInterpolator`
- Pros: Well-tested, handles multi-dimensional output naturally
- Cons: Less control over internals

### Approach 2: Custom NumPy Implementation
- Implement RBF training from scratch
- Pros: Full control, educational, can optimize for our use case
- Cons: More development time, need to handle edge cases

### Approach 3: Scikit-learn RBF Kernel
- Use `sklearn.kernel_ridge.KernelRidge` with RBF kernel
- Pros: Includes regularization, well-documented
- Cons: Designed for classification/regression, may be overkill

---

## Data Pipeline

### Input Format
- MOCAP data: Position/rotation data over time
- Extract: End effector positions (hands/feet)
- Extract: Corresponding pole vector positions (from existing rig)

### Processing
1. Parse MOCAP data (Python)
2. Extract relevant joint positions (end effector, pole vector)
3. Build training dataset: (end_effector_pos) → (pole_vector_pos)
4. Normalize data (store normalization params)
5. Train RBF interpolator (scipy or custom)
6. Validate with test/holdout data
7. Export model (centers, weights, params) to file

### Model File
- **Format**: JSON (initially), may switch to binary for production
- **Contents**: Centers, weights, kernel type, epsilon, normalization params
- **Location**: User-specified path (not embedded in plugin)

### Runtime Evaluation (C++ Plugin)
1. Load model file on demand
2. Receive end effector position from Maya rig
3. Normalize input using stored params
4. Evaluate RBF: `Σ wi * φ(||x - ci||)`
5. Denormalize output
6. Return predicted pole vector position to rig

---

## Development Environment

### R&D Phase
- Python 3.8+ (for compatibility with DCC tools)
- Jupyter notebooks for experimentation
- Standard scientific Python stack

### Production Phase (Future)
- **C++ Plugin Development**
  - Maya C++ API/SDK
  - Compiler: Visual Studio (Windows), Clang/GCC (Mac/Linux)
  - Maya version targeting: TBD (affects API version)
- **Performance Optimization**
  - SIMD vectorization for distance computations
  - Spatial indexing (KD-tree) for sparse evaluation
  - Multi-threading (if evaluating multiple limbs)
- **Distribution**
  - Compiled plugin (.mll for Windows, .bundle for Mac)
  - Model files (separate from plugin)
  - Documentation for animators

---

## Open Questions

1. **Basis Function Choice**: Which RBF kernel is best for this application?
   - Gaussian: `φ(r) = exp(-(εr)²)`
   - Multiquadric: `φ(r) = √(1 + (εr)²)`
   - Thin Plate Spline: `φ(r) = r² log(r)`
   - Inverse Multiquadric: `φ(r) = 1/√(1 + (εr)²)`
   - **Need to test**: Accuracy vs. computational cost

2. **Model File Format**: JSON vs. Binary vs. HDF5?
   - Start with JSON for development
   - Consider binary for production if file size/load time is an issue

3. **Dimensionality**: Input features beyond position?
   - Just end effector position (3D)?
   - Include shoulder/hip position for context?
   - Include character orientation?
   - Temporal features (velocity, previous poses)?

4. **Generalization**: Train per-character or universal model?
   - May need character-specific models due to proportions
   - Or normalize by character scale/proportions

5. **Data Requirements**: How many MOCAP samples needed?
   - Expect thousands of points
   - Need to determine through experimentation
   - May vary by limb (arms vs. legs)

6. **Performance Optimization**: When do we need spatial indexing?
   - At what N (number of centers) does O(N) become too slow?
   - Benchmark pure evaluation vs. k-nearest-neighbor approximation

---

## Next Steps
1. Install Python scientific stack
2. Test scipy.interpolate.RBFInterpolator with toy data
3. Generate synthetic test cases (simple arm reaching motions)
4. Evaluate different RBF kernels

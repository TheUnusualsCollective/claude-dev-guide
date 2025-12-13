# The Directives System

Directives provide Claude with detailed contextual operating guidelines. They are broken up into separate files to reduce token consumption. This is done by providing Claude with detailed high level instructions about how, when and under which circumstances particular directives should be read. These instructions are located  in [CLAUDE.md](CLAUDE.md#Directives).

## Token Economics

This is a breakdown of code consumption, based on 5 typical usage scenarios.

Since Claude *should* only load necessary directives, this gives

| Scenario              | Tokens  | What's Loaded                                       |
| --------------------- | ------- | --------------------------------------------------- |
| Quick                 | ~1,225  | quick-ref only                                      |
| Function design       | ~3,345  | quick-ref + function-design + code-reuse            |
| Refactoring           | ~5,290  | quick-ref + refactoring + code-reuse + antipatterns |
| Problem solving       | ~2,750  | quick-ref + problem-isolation + coordinate-transforms |
| New feature           | ~10,000 | quick-ref + 5-6 relevant coding directives          |
| All coding directives | ~11,000 | quick-ref + all 7 coding categories                 |
| Everything            | ~21,000 | all directive files                                 |

Total all directives: ~16,010 words ≈ 21,000 tokens (as of 2025-12-13)

The modular structure means 3,000-5,000 tokens will be loaded for the most common use cases, instead of the full 21,000.

## Upfront Cost
There is a definite cost to using detailed directives. However, without them, you'll just end up with slop. The directives save a great deal of work on the back end. Without specific guidance it's possible to have a machine make something that works. You can probably make 10 or 100 things that work, but more than likely, they will not work together. They will not be formatted the way you want. There will be no architectural form and there will be no design pattern. It will be slop, and the slop is expensive to clean up.
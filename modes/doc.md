# Mode: doc — Documentation
JSDoc inline comments + README.md per component/feature. Both in-repo.
Placement: component docs IN component folder; high-level → docs/ (create if missing). NEVER project root — co-located docs stay maintained.
JSDoc every exported function/class/constant: description, @param, @returns, @throws, @example. @typedef for complex objects.
README structure: Title → Purpose → Usage (examples first, 80% case) → API Reference → Integration Points → Implementation Notes → Testing.
Lead with examples — prose without code is skipped. "Why" not "what" — "what" is in the code.
DO: Every public API; copy-paste examples; integration points; error conditions.
NEVER: Vague descriptions; skip examples; private internals; excess prose; docs in root.

# 001 - Spec-Based Development

**Purpose:** Document new features in structured specs before implementation to ensure consistency and enable design review

**Requirements:**
- Write specs before coding new features
- Use sequential numbering (001, 002, 003...)
- Include design rationale and key decisions
- Keep specs focused on design, not implementation details
- Reference spec numbers in commit messages during implementation

**Design Approach:**
- Files named `XXX-{feature-name}.md` in `docs/spec/`
- Standard template focusing on purpose, requirements, design approach
- Status tracking: Draft -> Approved -> Implemented
- Update [000-shared-patterns.md] when specs introduce new patterns

**Implementation Notes:**
- See [000-shared-patterns.md] for code templates
- Specs should be under 100 lines when possible
- Extract shared patterns rather than repeating across specs
- Focus on "why" decisions were made, not "how" to implement

**Status:** Implemented

# 000 - Shared Patterns Reference

This document contains templates and boilerplate code that specs can reference to avoid repetition.

## Spec Template

Standard template for new specification documents:

```markdown
# XXX - Feature Name

**Purpose:** One-line description of what this does and why

**Requirements:**
- Key functional requirement 1
- Key functional requirement 2
- Important constraints or non-functional requirements

**Design Approach:**
- High-level design decision 1
- High-level design decision 2
- Key technical choices and rationale

**Implementation Notes:**
- Critical implementation details only
- Dependencies or special considerations
- Integration points with existing code

**Status:** [Draft/Approved/Implemented]
```

## Test Function Template

Standard test structure (table-driven, stdlib only):

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn feature_cases() {
        struct Case {
            name: &'static str,
            input: &'static str,
            want: Result<&'static str, &'static str>,
        }

        let cases = [
            Case { name: "happy path", input: "x", want: Ok("X") },
            Case { name: "empty input", input: "", want: Err("empty") },
        ];

        for c in cases {
            let got = feature(c.input);
            match (got, c.want) {
                (Ok(g), Ok(w)) => assert_eq!(g, w, "{}", c.name),
                (Err(_), Err(_)) => {}
                (g, w) => panic!("{}: got {:?}, want {:?}", c.name, g, w),
            }
        }
    }
}
```

### unit: proved_here
```
id: proved_here
source: chapter3-print-standalone.html §X · fixture (a:b · em—dash "q")
kind: derivation
narration: |
  fixture narration.
visual_need: |
  fixture chain.
screen_contract: |
  required_steps:
    - id: def
      tex: "a=b"
      reason: "定義"
    - id: reduced
      tex: "b=c"
      depends_on: elsewhere.result
      recap_required: true
```

## end
(an h2 ends the unit region)

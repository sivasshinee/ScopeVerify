# ScopeVerify

This checks one thing on a RIGOL DS1000Z or MSO1000Z oscilloscope: DC gain on channel 1.

No real scope is connected. Each test has a checklist file in `sequences` with the settings and the pass limits. The program reads that file, writes the remote commands into a list, and a pretend scope answers. The answer is the value that was just applied. A gain error can make that answer wrong on purpose. The program compares the answer with the limit and marks pass or fail.

## Manuals

Pass limits: MSO1000Z/DS1000Z Performance Verification Guide, September 2015, chapter 2, DC Gain Accuracy Test.

https://cdn-aorpci9.actonsoftware.com/acton/cdna/1579/f-0564/1/1/DS1000Z%20MSO1000Z%20Performance%20Verification%20Guide.pdf

Remote commands: MSO1000Z/DS1000Z Programming Guide, PGA19108-1110.

https://www.rigol.com/dam/global/downloads/brochures/en/program-guide/oscilloscopes/DS1000Z_ProgrammingGuide_EN.pdf

## Commands

```powershell
python -m unittest tests.test_dc_gain
python -m scope_verify
python -m scope_verify --gain-error 0.05
```

The first command should pass. The second prints a pass for every scale. The third pretends the scope reads 5% high: the 4% scales still pass, and the 3% scales fail.

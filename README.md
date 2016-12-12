# TinyParser
A parser for Tiny language

# How to use the scanner
- Make instance of it as following where `tiny_code` is the input code <br>
`s = TinyScanner(tiny_code)`
- You can scan the code using `scan` function which returns a string of (tokenvalue, tokentype)<br>
`output_str = s.scan()`
- You can save the output to a file using `createOutputFile` function<br>
` s.createOutputFile('out.txt')`

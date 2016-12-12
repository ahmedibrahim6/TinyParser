# TinyParser
A parser for Tiny language

# How to use the scanner
- Make instance of it as following where `tiny_code` is the input code <br>
`s = TinyScanner(tiny_code)`
- You can parse the code using `parse` function which retruns a string of (tokenvalue, tokentype)<br>
`output_str = s.parse()`
- You can save the output to a file using `createOutputFile` function<br>
` s.createOutputFile('out.txt')`

import re
s = '''<table class="reference">
<tbody><tr><th style="width:25%">实例</th><th>描述</th></tr>
<tr><td>[Pp]ython </td><td>匹配 "Python" 或 "python"</td></tr>
<tr><td>rub[ye]</td><td>匹配 "ruby" 或 "rube"</td></tr>
<tr><td>[aeiou]</td><td>匹配中括号内的任意一个字母</td></tr>
<tr><td>[0-9]</td><td>匹配任何数字。类似于 [0123456789]</td></tr>
<tr><td>[a-z]</td><td>匹配任何小写字母</td></tr>
<tr><td>[A-Z]</td><td>匹配任何大写字母</td></tr>
<tr><td>[a-zA-Z0-9]</td><td>匹配任何字母及数字</td></tr>
<tr><td>[^aeiou]</td><td>除了aeiou字母以外的所有字符 
</td></tr>
<tr><td>[^0-9]</td><td>匹配除了数字外的字符 
</td></tr>
</tbody></table>'''

reg = 
print(re.sub(r"<.*?>",'',s))
#python2
class Parser:
    def __init__(self):
        self.token=str
        #code=['if','number','<','identifier','then','identifier',':=','number',';','identifier',':=','number','end',' ']
        self.code=['identifier',':=','identifier','+','number','number']
        self.tmp_index=0
        self.token=self.code[self.tmp_index]

    def set_code(self,x):
        self.code=x
        self.tmp_index = 0
        self.token = self.code[self.tmp_index]

    def next_token(self):
        if(self.tmp_index==len(self.code)-1):
            return False  # we have reachd the end of the list
        self.tmp_index = self.tmp_index + 1
        self.token=self.code[self.tmp_index]
        return True

    def match(self,x):
        if self.token==x:
            self.next_token()
            return True
        else:
            raise ValueError('Token Mismatch',self.token)
            return False

    def stmt_sequence(self):
        self.statement()
        while self.token==';':
            self.match(';')
            if not self.statement():
                break

    def statement(self):
        if self.token=='if':
            self.if_stmt()
            return True
        elif self.token=='repeat':
            self.repeat_stmt()
            return True
        elif self.token=='identifier':
            self.assign_stmt()
            return True
        elif self.token=='read':
            self.read_stmt()
            return True
        elif self.token=='write':
            self.write_stmt()
            return True
        else:
            raise ValueError('SyntaxError',self.token)
            return False
            ##Error here


    def if_stmt(self):
        if self.token=='if':
            self.match('if')
            self.exp()
            self.match('then')
            self.stmt_sequence()
            if self.token=='else':
                self.stmt_sequence()
            self.match('end')

    def exp(self):
        self.simple_exp()
        if self.token=='<' or self.token=='>' or self.token=='=':
            self.comparison_op()
            self.simple_exp()

    def comparison_op(self):
        if self.token=='<':
            self.match('<')
        elif self.token=='>':
            self.match('>')
        elif self.token=='=':
            self.match('=')

    def simple_exp(self):
        self.term()
        while self.token=='+' or self.token=='-':
            self.addop()
            self.term()

    def addop(self):
        if self.token=='+':
            self.match('+')
        elif self.token=='-':
            self.match('-')

    def term(self):
        self.factor()
        while self.token=='*' or self.token=='/':
            self.mulop()
            self.factor()

    def mulop(self):
        if self.token=='*':
            self.match('*')
        elif self.token=='/':
            self.match('/')

    def factor(self):
        if self.token=='(':
            self.match('(')
            self.exp()
            self.match(')')
        elif self.token=='number':
            self.match('number')
        elif self.token=='identifier':
            self.match('identifier')
        else:
            raise ValueError('SyntaxError',self.token)
            return False

    def repeat_stmt(self):
        if self.token=='repeat':
            self.match('repeat')
            self.stmt_sequence()
            self.match('until')
            self.exp()

    def assign_stmt(self):
        self.match('identifier')
        self.match(':=')
        self.exp()

    def read_stmt(self):
        self.match('read')
        self.match('identifier')

    def write_stmt(self):
        self.match('write')
        self.exp()

    def run(self):
        self.stmt_sequence()
        if  self.tmp_index==len(self.code)-1:
            print'success'
        elif self.tmp_index<len(self.code):
            raise ValueError('SyntaxError',self.token)

p=Parser()
#p.set_code(['identifier',':=','identifier','+','number',';','identifier',':=','number','*','number'])
p.set_code(['if','number','<','identifier','then','identifier',':=','number',';','repeat',
            'identifier',':=','identifier','*','identifier',';','identifier',':=','identifier',
            '-','number','until','identifier','=','number',';','write','identifier','end'])
p.run()

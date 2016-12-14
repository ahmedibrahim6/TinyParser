#python2 & python3
class Node:
    def __init__(self,x):
        self.value = x
        self.children = []
        self.index=None

    def set_children(self,y):
        try:
            assert isinstance(y,list)
            for i in y:
                self.children.append(i)
        except:
            self.children.append(y)

class Parser:
    nodes_table={}
    tmp_index=0
    edges_table=[]

    def __init__(self):
        self.token=str
        self.code=['identifier',':=','identifier','+','number']
        self.tmp_index=0
        self.token=self.code[self.tmp_index]
        self.parse_tree=None
        self.nodes_table=None
        self.edges_table=None


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

    def stmt_sequence(self):
        t=self.statement()
        p=t
        while self.token==';':
            q=Node(None)
            self.match(';')
            q=self.statement()
            if q == None:
                break
            else:
                if t==None:
                    t=p=q
                else:
                    p.set_children(q)
                    p=q
        return t

    def statement(self):
        if self.token=='if':
            t=self.if_stmt()
            return t
        elif self.token=='repeat':
            t=self.repeat_stmt()
            return t
        elif self.token=='identifier':
            t=self.assign_stmt()
            return t
        elif self.token=='read':
            t=self.read_stmt()
            return t
        elif self.token=='write':
            t=self.write_stmt()
            return t
        else:
            raise ValueError('SyntaxError',self.token)
            ##Error here


    def if_stmt(self):
        t=Node('if')
        if self.token=='if':
            self.match('if')
            t.set_children(self.exp())
            self.match('then')
            t.set_children(self.stmt_sequence())
            if self.token=='else':
                t.set_children(self.stmt_sequence())
            self.match('end')
        return t

    def exp(self):
        t=self.simple_exp()
        if self.token=='<' or self.token=='>' or self.token=='=':
            p=Node(self.token)
            p.set_children(t)
            t=p
            self.comparison_op()
            t.set_children(self.simple_exp())
        return t

    def comparison_op(self):
        if self.token=='<':
            self.match('<')
        elif self.token=='>':
            self.match('>')
        elif self.token=='=':
            self.match('=')

    def simple_exp(self):
        t=self.term()
        while self.token=='+' or self.token=='-':
            p=Node('Opk')
            p.set_children(t)
            t=p
            self.addop()
            t.set_children(self.term())
        return t

    def addop(self):
        if self.token=='+':
            self.match('+')
        elif self.token=='-':
            self.match('-')

    def term(self):
        t=self.factor()
        while self.token=='*' or self.token=='/':
            p=Node('Opk')
            p.set_children(t)
            t=p
            self.mulop()
            p.set_children(self.factor())
        return t

    def mulop(self):
        if self.token=='*':
            self.match('*')
        elif self.token=='/':
            self.match('/')

    def factor(self):
        if self.token=='(':
            self.match('(')
            t=self.exp()
            self.match(')')
        elif self.token=='number':
            t=Node('ConstK')
            self.match('number')
        elif self.token=='identifier':
            t=Node('Idk')
            self.match('identifier')
        else:
            raise ValueError('SyntaxError',self.token)
            return False
        return t

    def repeat_stmt(self):
        t=Node('repeat')
        if self.token=='repeat':
            self.match('repeat')
            t.set_children(self.stmt_sequence())
            self.match('until')
            t.set_children(self.exp())
        return t

    def assign_stmt(self):
        t=Node('assign')
        self.match('identifier')
        self.match(':=')
        t.set_children(self.exp())
        return t

    def read_stmt(self):
        t=Node('read')
        self.match('read')
        self.match('identifier')
        return t

    def write_stmt(self):
        t=Node('write')
        self.match('write')
        t.set_children(self.exp())
        return t

    def create_nodes_table(self,args=None):
        if args==None:
            self.parse_tree.index=Parser.tmp_index
            Parser.nodes_table.update({Parser.tmp_index:self.parse_tree.value})
            Parser.tmp_index=Parser.tmp_index+1
            if len(self.parse_tree.children) !=0:
                for i in self.parse_tree.children:
                    self.create_nodes_table(i)
        else:
            args.index=Parser.tmp_index
            Parser.nodes_table.update({Parser.tmp_index:args.value})
            Parser.tmp_index=Parser.tmp_index+1
            if len(args.children) !=0:
                for i in args.children:
                    self.create_nodes_table(i)

    def create_edges_table(self,args=None):
        if args==None:
            if len(self.parse_tree.children)!=0:
                for i in self.parse_tree.children:
                    Parser.edges_table.append((self.parse_tree.index,i.index))
                for j in self.parse_tree.children:
                    self.create_edges_table(j)
        else:
            if len(args.children)!=0:
                for i in args.children:
                    Parser.edges_table.append((args.index,i.index))
                for j in args.children:
                    self.create_edges_table(j)



    def run(self):
        self.parse_tree=self.stmt_sequence()    #create parse tree
        self.create_nodes_table()               #create nodes_table
        self.create_edges_table()               #create edges_table
        self.edges_table=Parser.edges_table     #save edges_table
        self.nodes_table=Parser.nodes_table     #save nodes_table
        if  self.tmp_index==len(self.code)-1:
            print('success')
        elif self.tmp_index<len(self.code):
            raise ValueError('SyntaxError',self.token)



p=Parser()
#p.set_code(['identifier',':=','identifier','+','number',';','identifier',':=','number','*','number'])
p.set_code(['if','number','<','identifier','then','identifier',':=','number',';','repeat',
            'identifier',':=','identifier','*','identifier',';','identifier',':=','identifier',
            '-','number','until','identifier','=','number',';','write','identifier','end'])
#p.set_code(['if','identifier','<','number','then','identifier',':=','number','end'])
p.run()

print (p.nodes_table)
print (p.edges_table)

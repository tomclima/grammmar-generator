from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor:
    variables = {}
    def visit(self, ctx):
        if isinstance(ctx, ArithmeticParser.ProgramContext):
            return self.visitProgram(ctx)
        elif isinstance(ctx, ArithmeticParser.StatementContext):
            return self.visitStatement(ctx)
        elif isinstance(ctx, ArithmeticParser.AssignmentContext):
            return self.visitAssignment(ctx)
        elif isinstance(ctx, ArithmeticParser.ExprContext):
            return self.visitExpr(ctx)
        elif isinstance(ctx, ArithmeticParser.TermContext):
            return self.visitTerm(ctx)
        elif isinstance(ctx, ArithmeticParser.FactorContext):
            return self.visitFactor(ctx)

    def visitProgram(self, ctx):
        for i in range(0, len(ctx.statement())):
            self.visit(ctx.statement(i))
        
    def visitStatement(self, ctx):
        assignment = self.visit(ctx.assignment())
        if(assignment == None):
            self.visit(ctx.expr(0))

    def visitAssignment(self, ctx):
        variable = ctx.getChild(0).getText()
        self.variables[variable] = self.visit(ctx.expr())
        return self.variables[variable]

    def visitExpr(self, ctx):
        result = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            if ctx.getChild(i * 2 - 1).getText() == '+':
                result += self.visit(ctx.term(i))
            else:
                result -= self.visit(ctx.term(i))
        return result

    def visitTerm(self, ctx):
        result = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            if ctx.getChild(i * 2 - 1).getText() == '*':
                result *= self.visit(ctx.factor(i))
            else:
                result /= self.visit(ctx.factor(i))
        return result

    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            return self.variables[ctx.VAR().getText()]
        else:
            return self.visit(ctx.expr())

def main():
    with open("input.txt", "r") as file:
        program = file.read()
    lexer = ArithmeticLexer(InputStream(program))
    stream = CommonTokenStream(lexer)
    parser = ArithmeticParser(stream)
    tree = parser.program()
    visitor = ArithmeticVisitor()
    visitor.visit(tree)
    

if __name__ == '__main__':
    main()

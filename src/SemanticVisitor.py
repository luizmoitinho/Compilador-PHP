from AbstractVisitor import AbstractVisitor
import SymbolTable as st
from Visitor import Visitor

import SintaxeAbstrata as sa

def coercion(type1, type2):
  if (type1 in st.Number and type2 in st.Number):
      if (type1 == st.FLOAT or type2 == st.FLOAT):
          return st.FLOAT
      else:
          return st.INT
  else:
      return None


class SemanticVisitor(AbstractVisitor):
  
  def __init__(self):
    self.printer = Visitor()
    st.beginScope('global')
    
  def visitMain_MainInner(self, main):
    main.mainInner.accept(self)
    
  def visitMain_MainInner_Empty(self, main):
    st.endScope()
    
  def visitMainInner_InnerStatement_MainInner(self, mainInner):
    mainInner.innerStatement.accept(self)
    mainInner.mainInner.accept(self)
    
  def visitMainInner_InnerStatement(self, mainInner):
    mainInner.innerStatement.accept(self)
    
  def visitInnerStatement_FuncDecStatement(self, innerStatement):
    innerStatement.funcDecStatement.accept(self)
    
  def visitInnerStatement_Statement(self, innerStatement):
    innerStatement.statement.accept(self)
    
  def visitFuncDecStatement_Function(self, funcDecStatement):
    funcId = funcDecStatement.fds_id.accept(self)
    params = funcDecStatement.fds_parameter.accept(self)
    functionExists = st.getBindable(funcId)
    if functionExists == None:
      st.addFunction(funcId, params)
      st.beginScope(funcId)
      for i in range(0, len(params)):
        st.addVar(params[i])
      funcDecStatement.fds_statements.accept(self)
      st.endScope()
    else:
      print('ERROR: function', funcId, 'has already been declared.')
    
  def visitFds_id_withAmpersand(self, fds_id):
    return fds_id.id
    
  def visitFds_id_noAmpersand(self, fds_id):
    return fds_id.id
  
  def visitFds_parameter_noParameter(self):
    return {}
  
  def visitFds_parameter_withParameter(self, fds_parameter):
    return fds_parameter.parameter_list.accept(self)
    
  def visitParameterList_Parameter_Mul(self, parameterList):
    return parameterList.parameter.accept(self) + parameterList.parameter_list_colon_parameter.accept(self)
    
  def visitParameterList_Parameter_Single(self, parameterList):
    return parameterList.parameter.accept(self)
    
  def visitParameterListColonParameter_Mul(self, parameterListColonParameter):
    return parameterListColonParameter.parameter.accept(self) + parameterListColonParameter.parameterListColonParameter.accept(self)
  
  def visitParameterListColonParameter_Single(self, parameterListColonParameter):
    return parameterListColonParameter.parameter.accept(self)
    
  def visitParameter_Var(self, parameter):
    return [parameter.variable]
  
  def visitFds_statements_withStatements(self, fds_statements):
    return fds_statements.inner_statement_MUL.accept(self)
    
  def visitFds_statements_noStatements(self, fds_statements):
    return 
  
  def visitInnerStatementMul_Mul(self, innerStatementMul):
    innerStatementMul.innerStatement.accept(self)
    innerStatementMul.innerStatementMul.accept(self)
    
  def visitInnerStatementMul_Single(self, innerStatementMul):
    innerStatementMul.innerStatement.accept(self)
    
  def visitStatement_Expr(self, statement):
    return statement.expr.accept(self)
    
  def visitExpr_Expr1(self, expr):
    return expr.expr1.accept(self)
  
  def visitExpr_Expr3(self, expr):
    return expr.expr3.accept(self)
  
  def visitExpr3_Var_Assign_Expr(self, expr3):
    var = expr3.variable.accept(self)
    ass = expr3.assignOp.accept(self)
    expr = expr3.expr.accept(self)
    print(var, ass, expr)
    return var, ass, expr 
    
  def visitExpr1_Variable(self, expr1):
    return expr1.variable.accept(self) 
    
  def visitExpr1_FunctionCall(self, expr1):
    return expr1.functionCall.accept(self)
    
  def visitExpr1_True(self, expr1):
    return st.BOOL
  
  def visitExpr1_False(self, expr1):
    return st.BOOL
  
  def visitExpr1_Scalar(self, expr1):
    return expr1.scalar.accept(self)
    
  def visitVariable_Reference_Variable(self, variable):
    return variable.reference_variable.accept(self)
    
  def visitReferenceVariable_Compound(self, referenceVariable):
    return referenceVariable.compoundvariable.accept(self)
      
  def visitCompoundVariableSingle(self, singleVariable):
    variable = st.getBindable(singleVariable.variable)
    if(variable == None):
      st.addVar(singleVariable.variable)
      return singleVariable.variable #retorna o token variable
    return variable #retorna os dados da variável, caso já declarada

  def visitFunctionCall_NoParameter(self, functionCall):
    bindable = st.getBindable(functionCall.id)
    if bindable == None:
      print('ERROR: Function', functionCall.id,'called but never defined.')
      
  def visitFunctionCall_WithParameter(self, functionCall):
    bindable = st.getBindable(functionCall.id)
    if bindable == None:
      print('ERROR: Function', functionCall.id,'called but never defined.')
    if bindable != None and bindable[st.BINDABLE] == st.FUNCTION:
      params = functionCall.parameterList.accept(self)
      if len(params) != len(bindable[st.PARAMS]):
        print('ERROR: Number of parameters of function', functionCall.id, 'differs from declaration.')
        
  def visitFCParameterList_Single(self, fcParameterList):
    return fcParameterList.fcParameter.accept(self) 

  def visitFCParameterList_Mul(self, fcParameterList):
    return fcParameterList.fcParameter.accept(self), fcParameterList.fcColonParameter.accept(self)
    
  def visitFCParameterListColonParameter_Single(self, fcParameterListColonParameter):
    return [fcParameterListColonParameter.fcParameter.accept(self)]
    
  def visitFCParameterListColonParameter_Mul(self, fcParameterListColonParameter):
    return [fcParameterListColonParameter.fcParameter.accept(self)] + fcParameterListColonParameter.fcplColonParameter.accept(self)
  
  def visitFunctionCallParameter_Expr(self, functionCallParameter):
    return functionCallParameter.expr.accept(self)
    
  def visitFunctionCallParameter_AmpersandVariable(self, functionCallParameter):
    return functionCallParameter.variable
  
  def visitScalar_Token(self, scalar):
    if isinstance(scalar.token, int):
      return st.INT
    elif isinstance(scalar.token, float):
      return st.FLOAT
    elif isinstance(scalar.token, str):
      return st.STRING
    
  def visitAssignOperator_Token(self, assignOp):
    return assignOp.token
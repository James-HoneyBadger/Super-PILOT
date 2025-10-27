/// Safe Expression Evaluator for Time Warp IDE
/// 
/// This module provides secure mathematical expression evaluation without using eval().
/// Supports: operators, math functions, variables, parentheses.

use anyhow::{Result, anyhow};
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
enum Token {
    Number(f64),
    Variable(String),
    Function(String),
    Operator(char),
    LeftParen,
    RightParen,
    Comma,
}

/// Safe expression evaluator
pub struct ExpressionEvaluator {
    variables: HashMap<String, f64>,
}

impl ExpressionEvaluator {
    pub fn new() -> Self {
        Self {
            variables: HashMap::new(),
        }
    }
    
    pub fn with_variables(vars: HashMap<String, f64>) -> Self {
        Self { variables: vars }
    }
    
    pub fn set_variable(&mut self, name: String, value: f64) {
        self.variables.insert(name, value);
    }
    
    /// Evaluate a mathematical expression safely
    pub fn evaluate(&self, expr: &str) -> Result<f64> {
        let tokens = self.tokenize(expr)?;
        let rpn = self.to_rpn(tokens)?;
        self.evaluate_rpn(rpn)
    }
    
    fn tokenize(&self, expr: &str) -> Result<Vec<Token>> {
        let mut tokens = Vec::new();
        let mut chars = expr.chars().peekable();
        
        while let Some(&ch) = chars.peek() {
            match ch {
                ' ' | '\t' | '\n' => {
                    chars.next();
                }
                '0'..='9' | '.' => {
                    let mut num_str = String::new();
                    while let Some(&c) = chars.peek() {
                        if c.is_ascii_digit() || c == '.' {
                            num_str.push(c);
                            chars.next();
                        } else {
                            break;
                        }
                    }
                    tokens.push(Token::Number(num_str.parse()?));
                }
                'A'..='Z' | 'a'..='z' | '_' => {
                    let mut name = String::new();
                    while let Some(&c) = chars.peek() {
                        if c.is_alphanumeric() || c == '_' {
                            name.push(c);
                            chars.next();
                        } else {
                            break;
                        }
                    }
                    
                    // Check if it's a function (followed by '(')
                    if chars.peek() == Some(&'(') {
                        tokens.push(Token::Function(name.to_uppercase()));
                    } else {
                        tokens.push(Token::Variable(name.to_uppercase()));
                    }
                }
                '+' => {
                    tokens.push(Token::Operator('+'));
                    chars.next();
                }
                '-' => {
                    // Handle negative numbers - if minus is at start or after operator/left paren, treat as part of number
                    let is_unary = tokens.is_empty() || 
                        matches!(tokens.last(), Some(Token::Operator(_)) | Some(Token::LeftParen) | Some(Token::Comma));
                    
                    if is_unary && chars.clone().nth(1).map(|c| c.is_ascii_digit()).unwrap_or(false) {
                        chars.next(); // consume '-'
                        let mut num_str = String::from("-");
                        while let Some(&c) = chars.peek() {
                            if c.is_ascii_digit() || c == '.' {
                                num_str.push(c);
                                chars.next();
                            } else {
                                break;
                            }
                        }
                        tokens.push(Token::Number(num_str.parse()?));
                    } else {
                        tokens.push(Token::Operator('-'));
                        chars.next();
                    }
                }
                '*' | '/' | '^' | '%' => {
                    tokens.push(Token::Operator(ch));
                    chars.next();
                }
                '(' => {
                    tokens.push(Token::LeftParen);
                    chars.next();
                }
                ')' => {
                    tokens.push(Token::RightParen);
                    chars.next();
                }
                ',' => {
                    tokens.push(Token::Comma);
                    chars.next();
                }
                _ => return Err(anyhow!("Invalid character: {}", ch)),
            }
        }
        
        Ok(tokens)
    }
    
    fn to_rpn(&self, tokens: Vec<Token>) -> Result<Vec<Token>> {
        let mut output = Vec::new();
        let mut operator_stack: Vec<Token> = Vec::new();
        
        for token in tokens {
            match token {
                Token::Number(_) | Token::Variable(_) => output.push(token),
                Token::Function(_) => operator_stack.push(token),
                Token::Operator(op) => {
                    while let Some(top) = operator_stack.last() {
                        if let Token::Operator(top_op) = top {
                            if self.precedence(*top_op) >= self.precedence(op) {
                                output.push(operator_stack.pop().unwrap());
                            } else {
                                break;
                            }
                        } else if matches!(top, Token::Function(_)) {
                            break;
                        } else {
                            break;
                        }
                    }
                    operator_stack.push(Token::Operator(op));
                }
                Token::LeftParen => operator_stack.push(token),
                Token::RightParen => {
                    while let Some(top) = operator_stack.pop() {
                        if matches!(top, Token::LeftParen) {
                            break;
                        }
                        output.push(top);
                    }
                    
                    // Check for function
                    if let Some(Token::Function(_)) = operator_stack.last() {
                        output.push(operator_stack.pop().unwrap());
                    }
                }
                Token::Comma => {
                    while let Some(top) = operator_stack.last() {
                        if matches!(top, Token::LeftParen) {
                            break;
                        }
                        output.push(operator_stack.pop().unwrap());
                    }
                }
            }
        }
        
        while let Some(op) = operator_stack.pop() {
            output.push(op);
        }
        
        Ok(output)
    }
    
    fn evaluate_rpn(&self, rpn: Vec<Token>) -> Result<f64> {
        let mut stack: Vec<f64> = Vec::new();
        
        for token in rpn {
            match token {
                Token::Number(n) => stack.push(n),
                Token::Variable(name) => {
                    let val = self.variables
                        .get(&name)
                        .copied()
                        .ok_or_else(|| anyhow!("Undefined variable: {}", name))?;
                    stack.push(val);
                }
                Token::Operator(op) => {
                    let b = stack.pop().ok_or_else(|| anyhow!("Stack underflow"))?;
                    let a = stack.pop().ok_or_else(|| anyhow!("Stack underflow"))?;
                    
                    let result = match op {
                        '+' => a + b,
                        '-' => a - b,
                        '*' => a * b,
                        '/' => {
                            if b.abs() < f64::EPSILON {
                                return Err(anyhow!("Division by zero"));
                            }
                            a / b
                        }
                        '^' => a.powf(b),
                        '%' => a % b,
                        _ => return Err(anyhow!("Unknown operator: {}", op)),
                    };
                    
                    stack.push(result);
                }
                Token::Function(name) => {
                    let result = self.call_function(&name, &mut stack)?;
                    stack.push(result);
                }
                _ => return Err(anyhow!("Unexpected token in RPN")),
            }
        }
        
        stack.pop().ok_or_else(|| anyhow!("Empty stack"))
    }
    
    fn call_function(&self, name: &str, stack: &mut Vec<f64>) -> Result<f64> {
        match name {
            "SIN" => {
                let a = stack.pop().ok_or_else(|| anyhow!("SIN: missing argument"))?;
                Ok(a.sin())
            }
            "COS" => {
                let a = stack.pop().ok_or_else(|| anyhow!("COS: missing argument"))?;
                Ok(a.cos())
            }
            "TAN" => {
                let a = stack.pop().ok_or_else(|| anyhow!("TAN: missing argument"))?;
                Ok(a.tan())
            }
            "ATAN" | "ATN" => {
                let a = stack.pop().ok_or_else(|| anyhow!("ATAN: missing argument"))?;
                Ok(a.atan())
            }
            "SQRT" | "SQR" => {
                let a = stack.pop().ok_or_else(|| anyhow!("SQRT: missing argument"))?;
                Ok(a.sqrt())
            }
            "ABS" => {
                let a = stack.pop().ok_or_else(|| anyhow!("ABS: missing argument"))?;
                Ok(a.abs())
            }
            "EXP" => {
                let a = stack.pop().ok_or_else(|| anyhow!("EXP: missing argument"))?;
                Ok(a.exp())
            }
            "LOG" | "LN" => {
                let a = stack.pop().ok_or_else(|| anyhow!("LOG: missing argument"))?;
                Ok(a.ln())
            }
            "LOG10" => {
                let a = stack.pop().ok_or_else(|| anyhow!("LOG10: missing argument"))?;
                Ok(a.log10())
            }
            "INT" => {
                let a = stack.pop().ok_or_else(|| anyhow!("INT: missing argument"))?;
                Ok(a.floor())
            }
            "ROUND" => {
                let a = stack.pop().ok_or_else(|| anyhow!("ROUND: missing argument"))?;
                Ok(a.round())
            }
            "SGN" => {
                let a = stack.pop().ok_or_else(|| anyhow!("SGN: missing argument"))?;
                Ok(if a > 0.0 { 1.0 } else if a < 0.0 { -1.0 } else { 0.0 })
            }
            "RND" => {
                // Random number between 0 and 1
                Ok(rand::random::<f64>())
            }
            "MAX" => {
                let b = stack.pop().ok_or_else(|| anyhow!("MAX: missing argument"))?;
                let a = stack.pop().ok_or_else(|| anyhow!("MAX: missing argument"))?;
                Ok(a.max(b))
            }
            "MIN" => {
                let b = stack.pop().ok_or_else(|| anyhow!("MIN: missing argument"))?;
                let a = stack.pop().ok_or_else(|| anyhow!("MIN: missing argument"))?;
                Ok(a.min(b))
            }
            "POW" => {
                let b = stack.pop().ok_or_else(|| anyhow!("POW: missing argument"))?;
                let a = stack.pop().ok_or_else(|| anyhow!("POW: missing argument"))?;
                Ok(a.powf(b))
            }
            _ => Err(anyhow!("Unknown function: {}", name)),
        }
    }
    
    fn precedence(&self, op: char) -> u8 {
        match op {
            '+' | '-' => 1,
            '*' | '/' | '%' => 2,
            '^' => 3,
            _ => 0,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_basic_arithmetic() {
        let eval = ExpressionEvaluator::new();
        assert_eq!(eval.evaluate("2 + 3").unwrap(), 5.0);
        assert_eq!(eval.evaluate("10 - 4").unwrap(), 6.0);
        assert_eq!(eval.evaluate("3 * 4").unwrap(), 12.0);
        assert_eq!(eval.evaluate("15 / 3").unwrap(), 5.0);
    }
    
    #[test]
    fn test_precedence() {
        let eval = ExpressionEvaluator::new();
        assert_eq!(eval.evaluate("2 + 3 * 4").unwrap(), 14.0);
        assert_eq!(eval.evaluate("(2 + 3) * 4").unwrap(), 20.0);
    }
    
    #[test]
    fn test_functions() {
        let eval = ExpressionEvaluator::new();
        assert!((eval.evaluate("SIN(0)").unwrap() - 0.0).abs() < 0.0001);
        assert_eq!(eval.evaluate("ABS(-5)").unwrap(), 5.0);
        assert_eq!(eval.evaluate("SQRT(16)").unwrap(), 4.0);
    }
    
    #[test]
    fn test_variables() {
        let mut vars = HashMap::new();
        vars.insert("X".to_string(), 10.0);
        vars.insert("Y".to_string(), 5.0);
        let eval = ExpressionEvaluator::with_variables(vars);
        assert_eq!(eval.evaluate("X + Y").unwrap(), 15.0);
        assert_eq!(eval.evaluate("X * 2 + Y").unwrap(), 25.0);
    }
}

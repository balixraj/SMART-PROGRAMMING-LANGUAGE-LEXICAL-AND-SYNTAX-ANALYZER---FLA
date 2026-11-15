import unittest
from src.automata import identifier_dfa,number_dfa,delimiter_pda
from src.parser import analyze_program
class TestAnalyzer(unittest.TestCase):
 def test_ids(self):
  self.assertTrue(identifier_dfa("student_name")[0]); self.assertTrue(identifier_dfa("_x9")[0])
  self.assertFalse(identifier_dfa("2student")[0]); self.assertFalse(identifier_dfa("a-b")[0])
 def test_nums(self):
  self.assertTrue(number_dfa("123")[0]); self.assertTrue(number_dfa("45.67")[0])
  self.assertFalse(number_dfa(".5")[0]); self.assertFalse(number_dfa("5.")[0])
 def test_pda(self):
  self.assertTrue(delimiter_pda("([{}])")[0]); self.assertFalse(delimiter_pda("([)]")[0])
  self.assertFalse(delimiter_pda("((x)")[0])
 def test_cfg(self):
  self.assertTrue(analyze_program("x = a+b;")[0])
  self.assertTrue(analyze_program("if (x >= 10) { y = x; }")[0])
  self.assertFalse(analyze_program("x = + a;")[0])
  self.assertFalse(analyze_program("if (x 10) { y = 1; }")[0])
if __name__=="__main__": unittest.main()

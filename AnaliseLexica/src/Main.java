import java.util.ArrayList;
import java.util.Scanner;
import  java.util.ArrayList;

public class Main {
	public static void main(String Args[]) {
		ArrayList<Token> tokens =  new ArrayList<Token>();
		Lexer lexer =  new Lexer("if a");
//		while(lexer.buffer.getPosAtual() <  lexer.buffer.lexema.length())
		System.out.println(lexer.proximoToken().toString());
		System.out.println(lexer.proximoToken().toString());
		System.out.println(lexer.proximoToken().toString());
	}
}
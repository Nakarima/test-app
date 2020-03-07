package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
	"unicode"
)

func postfixEvaluation(expression []string) string {
	if len(expression) == 1 {
		return expression[0]
	}

	stack := []string{}
	operators := map[string]func(x float64, y float64) float64{
		"+": func(x float64, y float64) float64 { return x + y },
		"-": func(x float64, y float64) float64 { return x - y },
		"*": func(x float64, y float64) float64 { return x * y },
		"/": func(x float64, y float64) float64 { return x / y },
	}

	for _, s := range expression {
		if _, err := strconv.ParseFloat(s, 64); err == nil {
			stack = append(stack, s)
		} else {
			s2, _ := strconv.ParseFloat(stack[len(stack)-1], 64)
			stack = stack[:len(stack)-1]
			s1, _ := strconv.ParseFloat(stack[len(stack)-1], 64)
			stack = stack[:len(stack)-1]
			stack = append(stack, strconv.FormatFloat(operators[s](s1, s2), 'f', -1, 64))
		}
	}

	return stack[0]
}

func postfixTransform(expression string) ([]string, error) {
	postfix := []string{}
	stack := []string{}
	operators := "+-/*"
	prec := map[string]int{
		"*": 3,
		"/": 3,
		"+": 2,
		"-": 2,
		"(": 1,
	}

	expression = strings.ReplaceAll(expression, " ", "")
	//dirty, strings conv everywhere xD
	for i, s := range expression {
		if unicode.IsDigit(s) {
			if unicode.IsDigit(rune(expression[i-1])) {
				postfix[len(postfix)-1] = postfix[len(postfix)-1] + string(s)
			} else {
				postfix = append(postfix, string(s))
			}
		} else if strings.ContainsAny(string(s), operators) {
			for len(stack) > 0 && prec[string(s)] <= prec[stack[len(stack)-1]] {
				postfix = append(postfix, stack[len(stack)-1])
				stack = stack[:len(stack)-1]
			}
			stack = append(stack, string(s))
		} else if strings.ContainsAny(string(s), "(") {
			stack = append(stack, string(s))
		} else if strings.ContainsAny(string(s), ")") {
			o := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			for !strings.ContainsAny(string(o), "(") {
				postfix = append(postfix, o)
				if len(stack) > 0 {
					o = stack[len(stack)-1]
					stack = stack[:len(stack)-1]
				} else {

					return nil, errors.New("unclosed parenthisis")
				}
			}
			if len(stack) > 0 && strings.ContainsAny(stack[len(stack)-1], operators) {
				postfix = append(postfix, stack[len(stack)-1])
				stack = stack[:len(stack)-1]
			}

		} else {
			return nil, errors.New("char not allowed")
		}

	}

	for len(stack) > 0 {
		postfix = append(postfix, stack[len(stack)-1])
		stack = stack[:len(stack)-1]
	}

	return postfix, nil
}

func main() {

	reader := bufio.NewReader(os.Stdin)
	input, _ := reader.ReadString('\n')
	input = strings.ReplaceAll(input, "\n", "")
	text, err := postfixTransform(input)

	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(postfixEvaluation(text))
	}
}

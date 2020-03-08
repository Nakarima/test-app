package main

import (
	"encoding/json"
	"errors"
	"github.com/gorilla/mux"
	"log"
	"net/http"
	"strconv"
	"strings"
	"unicode"
)

type exprStruct struct {
	Expression string
}

func calc(expression string) (string, error) {
	expr, err := postfixTransform(expression)

	if err != nil {
		return "", err
	}
	c := make(chan string)
	go expressionEvaluation(expr, c)

	res := <-c
	return res, nil
}

func expressionEvaluation(expression []string, c chan string) {
	if len(expression) < 7 {
		c <- postfixEvaluation(expression)
		return
	}

	lastOperator := expression[len(expression)-1]
	expression = expression[:len(expression)-1]
	operandsCount := 0
	operatorsCount := 1
	index := len(expression) - 1

	for operatorsCount != operandsCount {
		if strings.ContainsAny(expression[index], "+-/*") {
			operatorsCount++
		} else {
			operandsCount++
		}
		index--
	}

	expr1 := expression[index+1:]
	expr2 := expression[:index+1]
	chan1 := make(chan string)
	chan2 := make(chan string)

	go expressionEvaluation(expr1, chan1)
	go expressionEvaluation(expr2, chan2)

	res1 := <-chan1
	res2 := <-chan2
	c <- postfixEvaluation([]string{res1, res2, lastOperator})
	return
}

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
			if i > 0 && unicode.IsDigit(rune(expression[i-1])) {
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
		o := stack[len(stack)-1]
		if o == "(" {
			return nil, errors.New("unclosed parenthisis")
		}
		postfix = append(postfix, stack[len(stack)-1])
		stack = stack[:len(stack)-1]
	}

	if len(postfix)%2 == 0 {
		return nil, errors.New("too many operators")
	}

	return postfix, nil
}

func evaluate(w http.ResponseWriter, r *http.Request) {
	decoder := json.NewDecoder(r.Body)
	var expr exprStruct
	err := decoder.Decode(&expr)
	if err != nil {
		w.WriteHeader(420)
		json.NewEncoder(w).Encode(err.Error())
		return
	}

	result, err := calc(expr.Expression)
	if err != nil {
		w.WriteHeader(420)
		json.NewEncoder(w).Encode(err.Error())
		return
	}

	json.NewEncoder(w).Encode(result)
	return
}

func handleRequests() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/evaluate", evaluate).Methods("POST")
	log.Fatal(http.ListenAndServe(":5000", router))
}

func main() {
	handleRequests()
}

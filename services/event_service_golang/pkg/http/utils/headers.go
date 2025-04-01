package utils

import (
	"fmt"
	"log/slog"
	"net/http"
	"strconv"
)

func ValidateHeaders(headersList map[string]string, log *slog.Logger, r *http.Request) (map[string]interface{}, error) {
	convertFuncs := map[string]func(string) (interface{}, error){
		"int":  func(value string) (interface{}, error) { return strconv.Atoi(value) },
		"bool": func(value string) (interface{}, error) { return strconv.ParseBool(value) },
	}

	resultMap := make(map[string]interface{})
	for key, expectedType := range headersList {
		log.Debug(key, expectedType)

		actualKey := r.Header.Get(key)
		if actualKey == "" {
			log.Error("Invalid request header")

			return nil, fmt.Errorf("absent header: %s", expectedType)
		}

		convertFunc, exists := convertFuncs[expectedType]
		if !exists {
			log.Error("Unsupported type:", slog.String("error", expectedType))

			return nil, fmt.Errorf("invalid type: %s", expectedType)
		}

		result, err := convertFunc(actualKey)
		if err != nil {
			log.Error("Failed to convert header:", slog.String("error", err.Error()))

			return nil, err
		}

		resultMap[key] = result
	}

	return resultMap, nil
}

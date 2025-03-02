package main

import (
	_ "event_service/cmd/event_service/docs"
	"event_service/internal/config"
	"event_service/internal/repositories"
	"event_service/internal/routes/rest"
	"event_service/internal/service"
	"fmt"
	"github.com/go-pg/pg/v10"
	httpSwagger "github.com/swaggo/http-swagger"
	"log/slog"
	"net/http"
	"os"
)

const (
	envLocal = "local"
	envDev   = "dev"
	envProd  = "prod"
)

func main() {
	cfg := config.MustLoad()
	fmt.Println(cfg)

	logger := setupLogger(cfg.Env)

	logger.Info("Starting event-service", slog.String("env", cfg.Env))
	logger.Debug("debug messages are enabled")

	db := pg.Connect(&pg.Options{
		Addr: cfg.SQLDatabase.Url,
	})

	dateRepository := repositories.NewDateRepository(db)
	dateService := service.NewDateService(dateRepository, db)
	handler := rest.New(logger, dateService)

	handler.Get("/swagger/*", httpSwagger.WrapHandler)

	logger.Info("starting server", slog.String("address", cfg.Address))

	server := &http.Server{
		Addr:         cfg.Address,
		Handler:      handler,
		ReadTimeout:  cfg.HTTPServer.Timeout,
		WriteTimeout: cfg.HTTPServer.Timeout,
		IdleTimeout:  cfg.HTTPServer.IdleTimeout,
	}

	if err := server.ListenAndServe(); err != nil {
		logger.Error("Failed to start server", err.Error())
	}

	logger.Error("server stopped")
}

func setupLogger(env string) *slog.Logger {
	var log *slog.Logger

	switch env {
	case envLocal:
		log = slog.New(
			slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelDebug}),
		)
	case envDev:
		log = slog.New(
			slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelDebug}),
		)
	case envProd:
		log = slog.New(
			slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}),
		)
	}

	return log
}

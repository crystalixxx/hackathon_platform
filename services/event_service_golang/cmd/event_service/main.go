package main

import (
	"event_service/internal/config"
	"event_service/internal/models"
	"event_service/internal/repositories"
	"event_service/internal/routes/rest"
	"event_service/internal/service"
	"fmt"
	"github.com/go-chi/chi/v5"
	"github.com/go-pg/pg/v10"
	"github.com/go-pg/pg/v10/orm"
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
		Addr:     cfg.SQLDatabase.Addr,
		User:     cfg.SQLDatabase.User,
		Password: cfg.SQLDatabase.Password,
		Database: cfg.SQLDatabase.Database,
	})

	InitM2M()

	router := chi.NewRouter()
	router.Mount("/event", createEventHandler(db, logger))
	router.Mount("/date", createDateHandler(db, logger))
	router.Mount("/status", createStatusHandler(db, logger))
	router.Mount("/location", createLocationHandler(db, logger))
	router.Mount("/track", createTrackHandler(db, logger))

	logger.Info("starting server", slog.String("address", cfg.Address))

	server := &http.Server{
		Addr:         cfg.Address,
		Handler:      router,
		ReadTimeout:  cfg.HTTPServer.Timeout,
		WriteTimeout: cfg.HTTPServer.Timeout,
		IdleTimeout:  cfg.HTTPServer.IdleTimeout,
	}

	if err := server.ListenAndServe(); err != nil {
		logger.Error("Failed to start server", err.Error())
	}

	logger.Error("server stopped")
}

func InitM2M() {
	orm.RegisterTable((*models.EventLocation)(nil))
	orm.RegisterTable((*models.StatusEvent)(nil))
	orm.RegisterTable((*models.StatusTrack)(nil))
	orm.RegisterTable((*models.EventPrize)(nil))
	orm.RegisterTable((*models.TeamActionStatus)(nil))
	orm.RegisterTable((*models.TrackJudge)(nil))
	orm.RegisterTable((*models.TrackWinner)(nil))
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

func createDateHandler(db *pg.DB, logger *slog.Logger) *chi.Mux {
	dateRepository := repositories.NewDateRepository(db)
	dateService := service.NewDateService(dateRepository, db)

	return rest.NewDate(logger, dateService)
}

func createEventHandler(db *pg.DB, logger *slog.Logger) *chi.Mux {
	statusEventRepository := repositories.NewStatusEventRepository(db)
	eventRepository := repositories.NewEventRepository(db)

	eventService := service.NewEventsService(eventRepository, statusEventRepository, db)
	return rest.NewEvent(logger, eventService)
}

func createStatusHandler(db *pg.DB, logger *slog.Logger) *chi.Mux {
	statusRepository := repositories.NewStatusRepository(db)
	statusService := service.NewStatusService(statusRepository, db)

	return rest.NewStatus(logger, statusService)
}

func createLocationHandler(db *pg.DB, logger *slog.Logger) *chi.Mux {
	locationRepository := repositories.NewLocationRepository(db)
	locationService := service.NewLocationService(locationRepository, db)

	return rest.NewLocation(logger, locationService)
}

func createTrackHandler(db *pg.DB, logger *slog.Logger) *chi.Mux {
	trackRepository := repositories.NewTrackRepository(db)
	trackService := service.NewTrackService(trackRepository, db)

	return rest.NewTrack(logger, trackService)
}

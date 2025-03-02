package rest

import (
	"encoding/json"
	"event_service/internal/models"
	"event_service/internal/schemas"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"log/slog"
	"net/http"
)

type EventService interface {
	GetAllEvents() ([]*models.Event, error)
	GetEventByID(id int) (*models.Event, error)
	CreateEvent(event schemas.Event) (*models.Event, error)
	UpdateEventTitle(eventID int, title string) (*models.Event, error)
	UpdateEventDescription(eventID int, description string) (*models.Event, error)
	UpdateRedirectLink(eventID int, redirectLink string) (*models.Event, error)
	UpdateDateID(eventID int, dateID int) (*models.Event, error)
	StartEvent(eventID int) (*models.Event, error)
	StopEvent(eventID int) (*models.Event, error)
}

func NewEvent(log *slog.Logger, service EventService) *chi.Mux {
	r := chi.NewRouter()

	r.Use(middleware.RequestID)
	r.Use(middleware.Recoverer)
	r.Use(middleware.URLFormat)

	//validate := validator.New()

	r.Route("/events", func(r chi.Router) {
		r.Get("/", getAllEventsHandler(log, service))
		//r.Post("/", createEventHandler(log, service, validate))

		//r.Route("/{id}", func(r chi.Router) {
		//r.Get("/", getEventByIDHandler(log, service))
		//r.Put("/", updateEventHandler(log, service, validate))
		//r.Delete("/", deleteEventHandler(log, service))
		//})
	})

	return r
}

func getAllEventsHandler(log *slog.Logger, service EventService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.getAll"

		log := log.With(
			slog.With("op", op),
			slog.With("request_id", middleware.GetReqID(r.Context())),
		)

		events, err := service.GetAllEvents()
		if err != nil {
			log.Error("error getting all events:", err)

			http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(events); err != nil {
			log.Error("error encoding events:", err)

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("events successfully fetched")
	}
}

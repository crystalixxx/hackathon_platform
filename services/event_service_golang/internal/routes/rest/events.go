package rest

import (
	"encoding/json"
	"event_service/internal/models"
	"event_service/internal/schemas"
	"event_service/internal/service"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-playground/validator/v10"
	"log/slog"
	"net/http"
	"strconv"
)

type EventService interface {
	GetAllEvents() ([]*models.Event, error)
	GetEventByID(eventId int) (*models.Event, error)
	GetEventByStatus(status string) ([]*models.Event, error)
	CreateEvent(event schemas.Event) (*models.Event, error)
	UpdateEvent(eventId int, newEvent schemas.EventUpdate) (*models.Event, error)
	DeleteEvent(eventID int) error
	StartEvent(eventID int) (*models.Event, error)
	EndEvent(eventID int) (*models.Event, error)
}

func NewEvent(log *slog.Logger, service *service.EventService) *chi.Mux {
	r := chi.NewRouter()

	r.Use(middleware.RequestID)
	r.Use(middleware.Recoverer)
	r.Use(middleware.URLFormat)
	r.Use(middleware.Logger)

	validate := validator.New()

	r.Route("/", func(r chi.Router) {
		r.Get("/", getAllEventsHandler(log, service))
		r.Post("/", createEventHandler(log, service, validate))

		r.Route("/{id}", func(r chi.Router) {
			r.Get("/", getEventByIDHandler(log, service))
			r.Put("/", updateEventHandler(log, service, validate))
			r.Delete("/", deleteEventHandler(log, service))
		})
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

func getEventByIDHandler(log *slog.Logger, service EventService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.getByID"

		log := log.With(
			slog.String("op", op),
			slog.String("request_it", middleware.GetReqID(r.Context())),
		)

		eventId, err := strconv.Atoi(chi.URLParam(r, "id"))
		date, err := service.GetEventByID(eventId)
		if err != nil {
			log.Error("Failed to get event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(date); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Event fetched successfully")
	}
}

func createEventHandler(log *slog.Logger, service EventService, validate *validator.Validate) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.create"

		log := log.With(
			slog.String("op", op),
			slog.String("request_it", middleware.GetReqID(r.Context())),
		)

		var date schemas.Event
		if err := decodeAndValidate(r, &date, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		resp, err := service.CreateEvent(date)
		if err != nil {
			log.Error("Failed to create event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusCreated)
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Event created successfully")
	}
}

func updateEventHandler(log *slog.Logger, service EventService, validate *validator.Validate) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.update"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		eventId, err := strconv.Atoi(chi.URLParam(r, "id"))

		var event schemas.EventUpdate
		if err := decodeAndValidate(r, &event, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		resp, err := service.UpdateEvent(eventId, event)
		if err != nil {
			log.Error("Failed to update event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Event updated successfully")
	}
}

func deleteEventHandler(log *slog.Logger, service EventService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.delete"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		dateId, err := strconv.Atoi(chi.URLParam(r, "id"))
		err = service.DeleteEvent(dateId)

		if err != nil {
			log.Error("Failed to delete date:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		log.Info("Event deleted successfully")
	}
}

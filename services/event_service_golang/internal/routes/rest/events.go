package rest

import (
	"encoding/json"
	"event_service/internal/models"
	"event_service/internal/schemas"
	"event_service/internal/service"
	"event_service/pkg/http/utils"
	"fmt"
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
	GetAllEventStatuses(eventID int) ([]*models.Status, error)
	AddStatusToEvent(statusEventSchema *schemas.StatusEvent) (*models.StatusEvent, error)
	RemoveStatusFromEvent(statusEventSchema *schemas.StatusEvent) error
	GetAllEventLocations(eventId int) ([]*models.Location, error)
	AddLocationToEvent(locationEventSchema *schemas.EventLocation) (*models.EventLocation, error)
	RemoveLocationFromEvent(statusEventSchema *schemas.EventLocation) error
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

		r.Route("/status", func(r chi.Router) {
			r.Post("/", addStatusToEventHandler(log, service))

			r.Route("/{id}", func(r chi.Router) {
				r.Get("/", getAllEventStatusesHandler(log, service))
				r.Delete("/", removeStatusFromEventHandler(log, service))
			})
		})

		r.Route("/location", func(r chi.Router) {
			r.Post("/", addLocationToEventHandler(log, service))

			r.Route("/{id}", func(r chi.Router) {
				r.Get("/", getAllEventLocationsHandler(log, service))
				r.Delete("/", removeLocationsFromEventHandler(log, service))
			})
		})

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
		event, err := service.GetEventByID(eventId)
		if err != nil {
			log.Error("Failed to get event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(event); err != nil {
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

		var event schemas.Event
		if err := decodeAndValidate(r, &event, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		resp, err := service.CreateEvent(event)
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

		trackId, err := strconv.Atoi(chi.URLParam(r, "id"))
		err = service.DeleteEvent(trackId)

		if err != nil {
			log.Error("Failed to delete event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		log.Info("Event deleted successfully")
	}
}

func getAllEventStatusesHandler(log *slog.Logger, service EventService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.statusGet"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		eventId, err := strconv.Atoi(chi.URLParam(r, "id"))
		statuses, err := service.GetAllEventStatuses(eventId)

		if err != nil {
			log.Error("Failed to get statuses by event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(statuses); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Statuses by event fetched successfully")
	}
}

func addStatusToEventHandler(log *slog.Logger, service EventService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.statusCreate"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		headersList := map[string]string{
			"EventId":  "int",
			"StatusId": "int",
		}

		convertedHeaders, err := utils.ValidateHeaders(headersList, log, r)
		if err != nil {
			log.Error("Failed to validate headers:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		newStatus, err := service.AddStatusToEvent(&schemas.StatusEvent{
			StatusID: convertedHeaders["StatusId"].(int),
			EventID:  convertedHeaders["EventId"].(int),
		})

		if err != nil {
			log.Error("Failed to add status to event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(newStatus); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Status added to event successfully")
	}
}

func removeStatusFromEventHandler(log *slog.Logger, service EventService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.statusDelete"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		queryParams := r.URL.Query()

		if queryParams.Get("status_id") == "" {
			log.Error("Missing 'status_id' in query")

			http.Error(w, "Missing 'status_id' in query", http.StatusBadRequest)
			return
		}

		eventId, err := strconv.Atoi(chi.URLParam(r, "id"))
		statusId, err := strconv.Atoi(queryParams.Get("status_id"))
		if err != nil {
			log.Error("Invalid format of status_id:", err.Error())

			http.Error(w, fmt.Sprintf("Invalid format of status_id query, expected number, got %s", queryParams.Get("status_id")), http.StatusBadRequest)
			return
		}

		err = service.RemoveStatusFromEvent(&schemas.StatusEvent{
			EventID:  eventId,
			StatusID: statusId,
		})

		if err != nil {
			log.Error("Failed to remove status from event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		log.Info("Status deleted from event successfully")
	}
}

func getAllEventLocationsHandler(log *slog.Logger, service EventService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.locationGet"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		locationId, err := strconv.Atoi(chi.URLParam(r, "id"))
		locations, err := service.GetAllEventLocations(locationId)

		if err != nil {
			log.Error("Failed to get locations by event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(locations); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Locations by event fetched successfully")
	}
}

func addLocationToEventHandler(log *slog.Logger, service EventService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.addLocation"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		headersList := map[string]string{
			"EventId":    "int",
			"LocationId": "int",
		}

		convertedHeaders, err := utils.ValidateHeaders(headersList, log, r)
		if err != nil {
			log.Error("Failed to validate headers:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		newLocation, err := service.AddLocationToEvent(&schemas.EventLocation{
			LocationID: convertedHeaders["LocationId"].(int),
			EventID:    convertedHeaders["EventId"].(int),
		})

		if err != nil {
			log.Error("Failed to add location to event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(newLocation); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Location added to event successfully")
	}
}

func removeLocationsFromEventHandler(log *slog.Logger, service EventService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.removeLocation"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		queryParams := r.URL.Query()

		if queryParams.Get("location_id") == "" {
			log.Error("Missing 'location_id' in query")

			http.Error(w, "Missing 'location_id' in query", http.StatusBadRequest)
			return
		}

		eventId, err := strconv.Atoi(chi.URLParam(r, "id"))
		locationId, err := strconv.Atoi(queryParams.Get("location_id"))
		if err != nil {
			log.Error("Invalid format of location_id:", err.Error())

			http.Error(w, fmt.Sprintf("Invalid format of location_id query, expected number, got %s", queryParams.Get("status_id")), http.StatusBadRequest)
			return
		}

		err = service.RemoveLocationFromEvent(&schemas.EventLocation{
			EventID:    eventId,
			LocationID: locationId,
		})

		if err != nil {
			log.Error("Failed to remove location from event:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		log.Info("Location deleted from event successfully")
	}
}

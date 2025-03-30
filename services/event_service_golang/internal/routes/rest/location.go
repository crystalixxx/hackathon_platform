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

type LocationService interface {
	GetAllLocations() ([]*models.Location, error)
	GetLocationById(locationId int) (*models.Location, error)
	CreateLocation(date schemas.Location) (*models.Location, error)
	UpdateLocation(locationId int, date schemas.LocationUpdate) (*models.Location, error)
	DeleteLocation(locationId int) error
}

func NewLocation(log *slog.Logger, service *service.LocationService) *chi.Mux {
	r := chi.NewRouter()

	r.Use(middleware.RequestID)
	r.Use(middleware.Recoverer)
	r.Use(middleware.URLFormat)
	r.Use(middleware.Logger)

	validate := validator.New()

	r.Route("/", func(r chi.Router) {
		r.Get("/", getAllLocationsHandler(log, service))
		r.Post("/", createLocationHandler(log, service, validate))

		r.Route("/{id}", func(r chi.Router) {
			r.Get("/", getLocationByIDHandler(log, service))
			r.Put("/", updateLocationHandler(log, service, validate))
			r.Delete("/", deleteLocationHandler(log, service))
		})
	})

	return r
}

func getAllLocationsHandler(log *slog.Logger, service LocationService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Location.getAll"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		location, err := service.GetAllLocations()
		if err != nil {
			log.Error("Failed to get locations:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(location); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Location fetched successfully")
	}
}

func getLocationByIDHandler(log *slog.Logger, service LocationService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Location.getByID"

		log := log.With(
			slog.String("op", op),
			slog.String("request_it", middleware.GetReqID(r.Context())),
		)

		locationId, err := strconv.Atoi(chi.URLParam(r, "id"))
		location, err := service.GetLocationById(locationId)
		if err != nil {
			log.Error("Failed to get location:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(location); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Location fetched successfully")
	}
}

func createLocationHandler(log *slog.Logger, service LocationService, validate *validator.Validate) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Location.create"

		log := log.With(
			slog.String("op", op),
			slog.String("request_it", middleware.GetReqID(r.Context())),
		)

		var location schemas.Location
		if err := decodeAndValidate(r, &location, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		resp, err := service.CreateLocation(location)
		if err != nil {
			log.Error("Failed to create location:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusCreated)
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Location created successfully")
	}
}

func updateLocationHandler(log *slog.Logger, service LocationService, validate *validator.Validate) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Location.update"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		var location schemas.LocationUpdate
		if err := decodeAndValidate(r, &location, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		locationId, err := strconv.Atoi(chi.URLParam(r, "id"))
		resp, err := service.UpdateLocation(locationId, location)

		if err != nil {
			log.Error("Failed to update location:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Location updated successfully")
	}
}

func deleteLocationHandler(log *slog.Logger, service LocationService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Location.delete"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		locationId, err := strconv.Atoi(chi.URLParam(r, "id"))
		err = service.DeleteLocation(locationId)

		if err != nil {
			log.Error("Failed to delete location:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		log.Info("Location deleted successfully")
	}
}

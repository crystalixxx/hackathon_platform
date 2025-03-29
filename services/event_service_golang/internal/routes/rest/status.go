package rest

import (
	"encoding/json"
	"event_service/internal/models"
	"event_service/internal/schemas"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-playground/validator/v10"
	"log/slog"
	"net/http"
	"strconv"
)

type StatusService interface {
	GetAllStatuses() ([]*models.Status, error)
	GetStatusById(id int) (*models.Status, error)
	CreateStatus(date schemas.Status) (*models.Status, error)
	UpdateStatus(id int, date schemas.Status) (*models.Status, error)
	DeleteStatus(id int) error
}

func NewStatus(log *slog.Logger, service StatusService) *chi.Mux {
	r := chi.NewRouter()

	r.Use(middleware.RequestID)
	r.Use(middleware.Recoverer)
	r.Use(middleware.URLFormat)
	r.Use(middleware.Logger)

	validate := validator.New()

	r.Route("/", func(r chi.Router) {
		r.Get("/", getAllStatusHandler(log, service))
		r.Post("/", createStatusHandler(log, service, validate))

		r.Route("/{id}", func(r chi.Router) {
			r.Get("/", getStatusByIDHandler(log, service))
			r.Put("/", updateStatusHandler(log, service, validate))
			r.Delete("/", deleteStatusHandler(log, service))
		})
	})

	return r
}

func getAllStatusHandler(log *slog.Logger, service StatusService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Status.getAll"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		statuses, err := service.GetAllStatuses()
		if err != nil {
			log.Error("Failed to get statuses:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(statuses); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Statuses fetched successfully")
	}
}

func getStatusByIDHandler(log *slog.Logger, service StatusService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Status.getByID"

		log := log.With(
			slog.String("op", op),
			slog.String("request_it", middleware.GetReqID(r.Context())),
		)

		statusId, err := strconv.Atoi(chi.URLParam(r, "id"))
		status, err := service.GetStatusById(statusId)
		if err != nil {
			log.Error("Failed to get status:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(status); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Status fetched successfully")
	}
}

func createStatusHandler(log *slog.Logger, service StatusService, validate *validator.Validate) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Status.create"

		log := log.With(
			slog.String("op", op),
			slog.String("request_it", middleware.GetReqID(r.Context())),
		)

		var status schemas.Status
		if err := decodeAndValidate(r, &status, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		resp, err := service.CreateStatus(status)
		if err != nil {
			log.Error("Failed to create date:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusCreated)
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Status created successfully")
	}
}

func updateStatusHandler(log *slog.Logger, service StatusService, validate *validator.Validate) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Status.update"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		var status schemas.Status
		if err := decodeAndValidate(r, &status, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		statusId, err := strconv.Atoi(chi.URLParam(r, "id"))
		resp, err := service.UpdateStatus(statusId, status)

		if err != nil {
			log.Error("Failed to update status:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Status updated successfully")
	}
}

func deleteStatusHandler(log *slog.Logger, service StatusService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Status.delete"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		statusId, err := strconv.Atoi(chi.URLParam(r, "id"))
		err = service.DeleteStatus(statusId)

		if err != nil {
			log.Error("Failed to delete status:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		log.Info("Status deleted successfully")
	}
}

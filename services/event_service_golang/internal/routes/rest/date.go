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

type DateService interface {
	GetAllDates() ([]*models.Date, error)
	GetDateByID(id int) (*models.Date, error)
	CreateDate(date schemas.Date) (*models.Date, error)
	UpdateDate(id int, date schemas.Date) (*models.Date, error)
	DeleteDate(id int) error
}

func NewDate(log *slog.Logger, service *service.DateService) *chi.Mux {
	r := chi.NewRouter()

	r.Use(middleware.RequestID)
	r.Use(middleware.Recoverer)
	r.Use(middleware.URLFormat)
	r.Use(middleware.Logger)

	validate := validator.New()

	r.Route("/", func(r chi.Router) {
		r.Get("/", getAllDatesHandler(log, service))
		r.Post("/", createDateHandler(log, service, validate))

		r.Route("/{id}", func(r chi.Router) {
			r.Get("/", getDateByIDHandler(log, service))
			r.Put("/", updateDateHandler(log, service, validate))
			r.Delete("/", deleteDateHandler(log, service))
		})
	})

	return r
}

func decodeAndValidate(r *http.Request, dst interface{}, validate *validator.Validate) error {
	if err := json.NewDecoder(r.Body).Decode(dst); err != nil {
		return err
	}

	return validate.Struct(dst)
}

func getAllDatesHandler(log *slog.Logger, service DateService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Date.getAll"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		dates, err := service.GetAllDates()
		if err != nil {
			log.Error("Failed to get dates:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(dates); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Dates fetched successfully")
	}
}

func getDateByIDHandler(log *slog.Logger, service DateService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Date.getByID"

		log := log.With(
			slog.String("op", op),
			slog.String("request_it", middleware.GetReqID(r.Context())),
		)

		dateId, err := strconv.Atoi(chi.URLParam(r, "id"))
		date, err := service.GetDateByID(dateId)
		if err != nil {
			log.Error("Failed to get date:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(date); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Date fetched successfully")
	}
}

func createDateHandler(log *slog.Logger, service DateService, validate *validator.Validate) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Date.create"

		log := log.With(
			slog.String("op", op),
			slog.String("request_it", middleware.GetReqID(r.Context())),
		)

		var date schemas.Date
		if err := decodeAndValidate(r, &date, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		resp, err := service.CreateDate(date)
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

		log.Info("Date created successfully")
	}
}

func updateDateHandler(log *slog.Logger, service DateService, validate *validator.Validate) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Date.update"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		var date schemas.Date
		if err := decodeAndValidate(r, &date, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		dateId, err := strconv.Atoi(chi.URLParam(r, "id"))
		resp, err := service.UpdateDate(dateId, date)

		if err != nil {
			log.Error("Failed to update date:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Date updated successfully")
	}
}

func deleteDateHandler(log *slog.Logger, service DateService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Date.delete"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		dateId, err := strconv.Atoi(chi.URLParam(r, "id"))
		err = service.DeleteDate(dateId)

		if err != nil {
			log.Error("Failed to delete date:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		log.Info("Date deleted successfully")
	}
}

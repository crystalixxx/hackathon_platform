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

type TrackService interface {
	GetAllTracks() ([]*models.Track, error)
	GetTrackById(trackId int) (*models.Track, error)
	CreateTrack(track schemas.Track) (*models.Track, error)
	UpdateTrack(trackId int, newTrack schemas.TrackUpdate) (*models.Track, error)
	DeleteTrack(trackId int) error
}

func NewTrack(log *slog.Logger, service *service.TrackService) *chi.Mux {
	r := chi.NewRouter()

	r.Use(middleware.RequestID)
	r.Use(middleware.Recoverer)
	r.Use(middleware.URLFormat)
	r.Use(middleware.Logger)

	validate := validator.New()

	r.Route("/", func(r chi.Router) {
		r.Get("/", getAllTracksHandler(log, service))
		r.Post("/", createTrackHandler(log, service, validate))

		r.Route("/{id}", func(r chi.Router) {
			r.Get("/", getTracksByIDHandler(log, service))
			r.Put("/", updateTrackHandler(log, service, validate))
			r.Delete("/", deleteTrackHandler(log, service))
		})
	})

	return r
}

func getAllTracksHandler(log *slog.Logger, service TrackService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Track.getAll"

		log := log.With(
			slog.With("op", op),
			slog.With("request_id", middleware.GetReqID(r.Context())),
		)

		tracks, err := service.GetAllTracks()
		if err != nil {
			log.Error("error getting all tracks:", err)

			http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(tracks); err != nil {
			log.Error("error encoding tracks:", err)

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("tracks successfully fetched")
	}
}

func getTracksByIDHandler(log *slog.Logger, service TrackService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Event.getByID"

		log := log.With(
			slog.String("op", op),
			slog.String("request_it", middleware.GetReqID(r.Context())),
		)

		trackId, err := strconv.Atoi(chi.URLParam(r, "id"))
		track, err := service.GetTrackById(trackId)
		if err != nil {
			log.Error("Failed to get track:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(track); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Track fetched successfully")
	}
}

func createTrackHandler(log *slog.Logger, service TrackService, validate *validator.Validate) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Track.create"

		log := log.With(
			slog.String("op", op),
			slog.String("request_it", middleware.GetReqID(r.Context())),
		)

		var track schemas.Track
		if err := decodeAndValidate(r, &track, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		resp, err := service.CreateTrack(track)
		if err != nil {
			log.Error("Failed to create track:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusCreated)
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Track created successfully")
	}
}

func updateTrackHandler(log *slog.Logger, service TrackService, validate *validator.Validate) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Track.update"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		trackId, err := strconv.Atoi(chi.URLParam(r, "id"))

		var track schemas.TrackUpdate
		if err := decodeAndValidate(r, &track, validate); err != nil {
			log.Error("Failed to decode request:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		resp, err := service.UpdateTrack(trackId, track)
		if err != nil {
			log.Error("Failed to update track:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Track updated successfully")
	}
}

func deleteTrackHandler(log *slog.Logger, service TrackService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Track.delete"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		trackId, err := strconv.Atoi(chi.URLParam(r, "id"))
		err = service.DeleteTrack(trackId)

		if err != nil {
			log.Error("Failed to delete track:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		log.Info("Track deleted successfully")
	}
}

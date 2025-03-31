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

type TrackService interface {
	GetAllTracks() ([]*models.Track, error)
	GetTrackById(trackId int) (*models.Track, error)
	CreateTrack(track schemas.Track) (*models.Track, error)
	UpdateTrack(trackId int, newTrack schemas.TrackUpdate) (*models.Track, error)
	DeleteTrack(trackId int) error
	GetAllTrackLocations(trackId int) ([]*models.Location, error)
	AddLocationToTrack(locationTrackSchema *schemas.LocationTrack) (*models.LocationTrack, error)
	RemoveLocationFromTrack(locationTrackSchema *schemas.LocationTrack) error
	GetAllTrackStatuses(trackId int) ([]*models.Status, error)
	AddStatusToTrack(statusTrackSchema *schemas.StatusTrack) (*models.StatusTrack, error)
	RemoveStatusFromTrack(statusTrackSchema *schemas.StatusTrack) error
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

		r.Route("/status", func(r chi.Router) {
			r.Post("/", addStatusToTrackHandler(log, service))

			r.Route("/{id}", func(r chi.Router) {
				r.Get("/", getAllTrackStatusesHandler(log, service))
				r.Delete("/", removeStatusFromTrackHandler(log, service))
			})
		})

		r.Route("/location", func(r chi.Router) {
			r.Post("/", addLocationToTrackHandler(log, service))

			r.Route("/{id}", func(r chi.Router) {
				r.Get("/", getAllTrackLocationsHandler(log, service))
				r.Delete("/", removeLocationFromTrackHandler(log, service))
			})
		})

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
		const op = "rest.Track.getByID"

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

func getAllTrackStatusesHandler(log *slog.Logger, service TrackService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Track.statusGet"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		trackId, err := strconv.Atoi(chi.URLParam(r, "id"))
		statuses, err := service.GetAllTrackStatuses(trackId)

		if err != nil {
			log.Error("Failed to get statuses by track:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(statuses); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Statuses by track fetched successfully")
	}
}

func addStatusToTrackHandler(log *slog.Logger, service TrackService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Track.statusCreate"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		headersList := map[string]string{
			"TrackId":  "int",
			"StatusId": "int",
		}

		convertedHeaders, err := utils.ValidateHeaders(headersList, log, r)
		if err != nil {
			log.Error("Failed to validate headers:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		newStatus, err := service.AddStatusToTrack(&schemas.StatusTrack{
			StatusID: convertedHeaders["StatusId"].(int),
			TrackID:  convertedHeaders["TrackId"].(int),
		})

		if err != nil {
			log.Error("Failed to add status to track:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(newStatus); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Status added to track successfully")
	}
}

func removeStatusFromTrackHandler(log *slog.Logger, service TrackService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Track.statusDelete"

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

		trackId, err := strconv.Atoi(chi.URLParam(r, "id"))
		statusId, err := strconv.Atoi(queryParams.Get("status_id"))
		if err != nil {
			log.Error("Invalid format of status_id:", err.Error())

			http.Error(w, fmt.Sprintf("Invalid format of status_id query, expected number, got %s", queryParams.Get("status_id")), http.StatusBadRequest)
			return
		}

		err = service.RemoveStatusFromTrack(&schemas.StatusTrack{
			TrackID:  trackId,
			StatusID: statusId,
		})

		if err != nil {
			log.Error("Failed to remove status from track:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		log.Info("Status deleted from track successfully")
	}
}

func getAllTrackLocationsHandler(log *slog.Logger, service TrackService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Track.locationGet"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		trackId, err := strconv.Atoi(chi.URLParam(r, "id"))
		locations, err := service.GetAllTrackLocations(trackId)

		if err != nil {
			log.Error("Failed to get locations by track:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(locations); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Locations by track fetched successfully")
	}
}

func addLocationToTrackHandler(log *slog.Logger, service TrackService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Track.addLocation"

		log := log.With(
			slog.String("op", op),
			slog.String("request_id", middleware.GetReqID(r.Context())),
		)

		headersList := map[string]string{
			"TrackId":    "int",
			"LocationId": "int",
		}

		convertedHeaders, err := utils.ValidateHeaders(headersList, log, r)
		if err != nil {
			log.Error("Failed to validate headers:", err.Error())

			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		newLocation, err := service.AddLocationToTrack(&schemas.LocationTrack{
			LocationId: convertedHeaders["LocationId"].(int),
			TrackId:    convertedHeaders["TrackId"].(int),
		})

		if err != nil {
			log.Error("Failed to add location to track:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		if err := json.NewEncoder(w).Encode(newLocation); err != nil {
			log.Error("Failed to encode response:", err.Error())

			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		}

		log.Info("Location added to track successfully")
	}
}

func removeLocationFromTrackHandler(log *slog.Logger, service TrackService) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		const op = "rest.Track.removeLocation"

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

		trackId, err := strconv.Atoi(chi.URLParam(r, "id"))
		locationId, err := strconv.Atoi(queryParams.Get("location_id"))
		if err != nil {
			log.Error("Invalid format of location_id:", err.Error())

			http.Error(w, fmt.Sprintf("Invalid format of location_id query, expected number, got %s", queryParams.Get("status_id")), http.StatusBadRequest)
			return
		}

		err = service.RemoveLocationFromTrack(&schemas.LocationTrack{
			TrackId:    trackId,
			LocationId: locationId,
		})

		if err != nil {
			log.Error("Failed to remove location from track:", err.Error())

			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		log.Info("Location deleted from track successfully")
	}
}

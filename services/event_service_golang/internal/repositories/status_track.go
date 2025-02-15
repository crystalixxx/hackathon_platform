package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type StatusTrackRepository struct {
	DB *pg.DB
}

func NewStatusTrackRepository(db *pg.DB) *StatusTrackRepository {
	return &StatusTrackRepository{DB: db}
}

func (r *StatusTrackRepository) Create(statusTrack *models.StatusTrack) error {
	_, err := r.DB.Model(statusTrack).Insert()
	return err
}

func (r *StatusTrackRepository) GetAllStatusTracks(StatusId int) ([]*models.StatusTrack, error) {
	statusTracks := make([]*models.StatusTrack, 0)
	err := r.DB.Model(&statusTracks).Where("status_id = ?", StatusId).Select()
	return statusTracks, err
}

func (r *StatusTrackRepository) GetAllTracksStatuses(TrackId int) ([]*models.StatusTrack, error) {
	statusTracks := make([]*models.StatusTrack, 0)
	err := r.DB.Model(&statusTracks).Where("track_id = ?", TrackId).Select()
	return statusTracks, err
}

func (r *StatusTrackRepository) DeleteStatusTrack(StatusId int, TrackId int) error {
	statusTrack := &models.StatusTrack{StatusID: StatusId, TrackID: TrackId}
	_, err := r.DB.Model(statusTrack).WherePK().Delete()
	return err
}

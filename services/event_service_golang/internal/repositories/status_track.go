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

func (r *StatusTrackRepository) Create(tx *pg.Tx, statusTrack *models.StatusTrack) error {
	_, err := tx.Model(statusTrack).Insert()
	return err
}

func (r *StatusTrackRepository) GetAllStatusTracks(tx *pg.Tx, StatusId int) ([]*models.StatusTrack, error) {
	statusTracks := make([]*models.StatusTrack, 0)
	err := tx.Model(&statusTracks).Where("status_id = ?", StatusId).Select()
	return statusTracks, err
}

func (r *StatusTrackRepository) GetAllTracksStatuses(tx *pg.Tx, TrackId int) ([]*models.StatusTrack, error) {
	statusTracks := make([]*models.StatusTrack, 0)
	err := tx.Model(&statusTracks).Where("track_id = ?", TrackId).Select()
	return statusTracks, err
}

func (r *StatusTrackRepository) DeleteStatusTrack(tx *pg.Tx, StatusId int, TrackId int) error {
	statusTrack := &models.StatusTrack{StatusID: StatusId, TrackID: TrackId}
	_, err := tx.Model(statusTrack).WherePK().Delete()
	return err
}

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

func (r *StatusTrackRepository) Create(tx *pg.Tx, statusTrack *models.StatusTrack) (*models.StatusTrack, error) {
	_, err := tx.Model(statusTrack).Insert()
	return statusTrack, err
}

func (r *StatusTrackRepository) GetAllStatusTracks(tx *pg.Tx, StatusId int) ([]*models.Status, error) {
	tracks := make([]*models.Status, 0)

	err := tx.Model(&tracks).
		Join("JOIN status_track se ON se.track_id = track.id").
		Where("se.status_id = ?", StatusId).
		Select()

	return tracks, err
}

func (r *StatusTrackRepository) GetAllTracksStatuses(tx *pg.Tx, TrackId int) ([]*models.Status, error) {
	statuses := make([]*models.Status, 0)

	err := tx.Model(&statuses).
		Join("JOIN status_track se ON se.status_id = status.id").
		Where("se.track_id = ?", TrackId).
		Select()

	return statuses, err
}

func (r *StatusTrackRepository) DeleteStatusTrack(tx *pg.Tx, StatusId int, TrackId int) error {
	statusTrack := &models.StatusTrack{StatusID: StatusId, TrackID: TrackId}
	_, err := tx.Model(statusTrack).WherePK().Delete()
	return err
}

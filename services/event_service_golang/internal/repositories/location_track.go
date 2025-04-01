package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type LocationTrackRepository struct {
	DB *pg.DB
}

func NewLocationTrackRepository(db *pg.DB) *LocationTrackRepository {
	return &LocationTrackRepository{DB: db}
}

func (r *LocationTrackRepository) Create(tx *pg.Tx, eventLocation *models.LocationTrack) (*models.LocationTrack, error) {
	_, err := tx.Model(eventLocation).Insert()
	return eventLocation, err
}

func (r *LocationTrackRepository) GetAllTracksLocations(tx *pg.Tx, TrackId int) ([]*models.Location, error) {
	locations := make([]*models.Location, 0)

	err := tx.Model(&locations).
		Join("JOIN location_track el ON el.location_id = location.id").
		Where("el.track_id = ?", TrackId).
		Select()

	return locations, err
}

func (r *LocationTrackRepository) GetAllLocationsTracks(tx *pg.Tx, LocationId int) ([]*models.Track, error) {
	tracks := make([]*models.Track, 0)

	err := tx.Model(&tracks).
		Join("JOIN location_track el ON el.track_id = track.id").
		Where("el.location_id = ?", LocationId).
		Select()

	return tracks, err
}

func (r *LocationTrackRepository) DeleteTrackLocation(tx *pg.Tx, TrackId int, LocationId int) error {
	tracksLocation := &models.LocationTrack{TrackId: TrackId, LocationId: LocationId}
	_, err := tx.Model(tracksLocation).WherePK().Delete()
	return err
}

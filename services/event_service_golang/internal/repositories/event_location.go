package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type EventLocationRepository struct {
	DB *pg.DB
}

func NewEventLocationRepository(db *pg.DB) *EventLocationRepository {
	return &EventLocationRepository{DB: db}
}

func (r *EventLocationRepository) Create(tx *pg.Tx, eventLocation *models.EventLocation) error {
	_, err := tx.Model(eventLocation).Insert()
	return err
}

func (r *EventLocationRepository) GetAllEventsLocations(tx *pg.Tx, EventId int) ([]*models.EventLocation, error) {
	eventLocations := make([]*models.EventLocation, 0)
	err := tx.Model(&eventLocations).Where("event_id = ?", EventId).Select()
	return eventLocations, err
}

func (r *EventLocationRepository) GetAllLocationsEvents(tx *pg.Tx, LocationId int) ([]*models.EventLocation, error) {
	eventLocations := make([]*models.EventLocation, 0)
	err := tx.Model(&eventLocations).Where("location_id = ?", LocationId).Select()
	return eventLocations, err
}

func (r *EventLocationRepository) DeleteEventLocation(tx *pg.Tx, EventId int, LocationId int) error {
	eventLocation := &models.EventLocation{EventID: EventId, LocationID: LocationId}
	_, err := tx.Model(eventLocation).WherePK().Delete()
	return err
}

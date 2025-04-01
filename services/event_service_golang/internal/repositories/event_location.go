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

func (r *EventLocationRepository) Create(tx *pg.Tx, eventLocation *models.EventLocation) (*models.EventLocation, error) {
	_, err := tx.Model(eventLocation).Insert()
	return eventLocation, err
}

func (r *EventLocationRepository) GetAllEventsLocations(tx *pg.Tx, EventId int) ([]*models.Location, error) {
	locations := make([]*models.Location, 0)

	err := tx.Model(&locations).
		Join("JOIN event_location el ON el.location_id = location.id").
		Where("el.event_id = ?", EventId).
		Select()

	return locations, err
}

func (r *EventLocationRepository) GetAllLocationsEvents(tx *pg.Tx, LocationId int) ([]*models.Event, error) {
	events := make([]*models.Event, 0)

	err := tx.Model(&events).
		Join("JOIN event_location el ON el.event_id = event.id").
		Where("el.location_id = ?", LocationId).
		Select()

	return events, err
}

func (r *EventLocationRepository) DeleteEventLocation(tx *pg.Tx, EventId int, LocationId int) error {
	eventLocation := &models.EventLocation{EventID: EventId, LocationID: LocationId}
	_, err := tx.Model(eventLocation).WherePK().Delete()
	return err
}

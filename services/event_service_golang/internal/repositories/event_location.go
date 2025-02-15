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

func (r *EventLocationRepository) Create(eventLocation *models.EventLocation) error {
	_, err := r.DB.Model(eventLocation).Insert()
	return err
}

func (r *EventLocationRepository) GetAllEventsLocations(EventId int) ([]*models.EventLocation, error) {
	eventLocations := make([]*models.EventLocation, 0)
	err := r.DB.Model(&eventLocations).Where("event_id = ?", EventId).Select()
	return eventLocations, err
}

func (r *EventLocationRepository) GetAllLocationsEvents(LocationId int) ([]*models.EventLocation, error) {
	eventLocations := make([]*models.EventLocation, 0)
	err := r.DB.Model(&eventLocations).Where("location_id = ?", LocationId).Select()
	return eventLocations, err
}

func (r *EventLocationRepository) DeleteEventLocation(EventId int, LocationId int) error {
	eventLocation := &models.EventLocation{EventID: EventId, LocationID: LocationId}
	_, err := r.DB.Model(eventLocation).WherePK().Delete()
	return err
}

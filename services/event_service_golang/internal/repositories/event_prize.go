package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type EventPrizeRepository struct {
	DB *pg.DB
}

func NewEventPrizeRepository(db *pg.DB) *EventPrizeRepository {
	return &EventPrizeRepository{DB: db}
}

func (r *EventPrizeRepository) Create(tx *pg.Tx, eventPrize *models.EventPrize) error {
	_, err := tx.Model(eventPrize).Insert()
	return err
}

func (r *EventPrizeRepository) GetAllEventPrizes(tx *pg.Tx) ([]*models.EventPrize, error) {
	eventPrizes := make([]*models.EventPrize, 0)
	err := tx.Model(&eventPrizes).Select()
	return eventPrizes, err
}

func (r *EventPrizeRepository) GetEventPrizesByEventID(tx *pg.Tx, eventID int) ([]*models.EventPrize, error) {
	eventPrizes := make([]*models.EventPrize, 0)
	err := tx.Model(&eventPrizes).Where("event_id = ?", eventID).Select()
	return eventPrizes, err
}

func (r *EventPrizeRepository) GetEventPrizeByID(tx *pg.Tx, eventPrizeID int) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	err := tx.Model(eventPrize).Where("id = ?", eventPrizeID).Select()
	return eventPrize, err
}

func (r *EventPrizeRepository) UpdateEventPrizePlace(tx *pg.Tx, eventPrizeID int, place int) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	_, err := tx.Model(eventPrize).Set("place = ?", place).Where("id = ?", eventPrizeID).Update()
	return eventPrize, err
}

func (r *EventPrizeRepository) UpdateEventPrizePrimaryPrize(tx *pg.Tx, eventPrizeID int, primaryPrize string) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	_, err := tx.Model(eventPrize).Set("primary_prize = ?", primaryPrize).Where("id = ?", eventPrizeID).Update()
	return eventPrize, err
}

func (r *EventPrizeRepository) UpdateEventPrizeDescription(tx *pg.Tx, eventPrizeID int, description string) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	_, err := tx.Model(eventPrize).Set("description = ?", description).Where("id = ?", eventPrizeID).Update()
	return eventPrize, err
}

func (r *EventPrizeRepository) UpdateEventPrizeIconURL(tx *pg.Tx, eventPrizeID int, iconURL string) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	_, err := tx.Model(eventPrize).Set("icon_url = ?", iconURL).Where("id = ?", eventPrizeID).Update()
	return eventPrize, err
}

func (r *EventPrizeRepository) UpdateEventPrizeEventID(tx *pg.Tx, eventPrizeID, eventID int) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	_, err := tx.Model(eventPrize).Set("event_id = ?", eventID).Where("id = ?", eventPrizeID).Update()
	return eventPrize, err
}

func (r *EventPrizeRepository) DeleteEventPrize(tx *pg.Tx, eventPrizeID int) error {
	eventPrize := new(models.EventPrize)
	_, err := tx.Model(eventPrize).Where("id = ?", eventPrizeID).Delete()
	return err
}

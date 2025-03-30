package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type StatusRepository struct {
	DB *pg.DB
}

func NewStatusRepository(db *pg.DB) *StatusRepository {
	return &StatusRepository{DB: db}
}

func (r *StatusRepository) Create(tx *pg.Tx, status *models.Status) (*models.Status, error) {
	_, err := tx.Model(status).Insert()
	return status, err
}

func (r *StatusRepository) GetAllStatuses(tx *pg.Tx) ([]*models.Status, error) {
	statuses := make([]*models.Status, 0)
	err := tx.Model(&statuses).Select()
	return statuses, err
}

func (r *StatusRepository) GetStatusById(tx *pg.Tx, id int) (*models.Status, error) {
	status := new(models.Status)
	err := tx.Model(status).Where("id = ?", id).Select()
	return status, err
}

func (r *StatusRepository) UpdateStatus(tx *pg.Tx, newStatus *models.Status) (*models.Status, error) {
	event := new(models.Status)
	_, err := tx.Model(event).Set("title = ?, description = ?", newStatus.Title, newStatus.Description).Returning("*").Update()
	return event, err
}

func (r *StatusRepository) DeleteStatus(tx *pg.Tx, id int) error {
	status := &models.Status{ID: id}
	_, err := tx.Model(status).WherePK().Delete()
	return err
}

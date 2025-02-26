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

func (r *StatusRepository) Create(tx *pg.Tx, status *models.Status) error {
	_, err := tx.Model(status).Insert()
	return err
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

func (r *StatusRepository) ChangeStatusTitle(tx *pg.Tx, id int, title string) (*models.Status, error) {
	status := new(models.Status)
	_, err := tx.Model(status).Set("title = ?", title).Where("id = ?", id).Update()
	return status, err
}

func (r *StatusRepository) ChangeStatusDescription(tx *pg.Tx, id int, description string) (*models.Status, error) {
	status := new(models.Status)
	_, err := tx.Model(status).Set("description = ?", description).Where("id = ?", id).Update()
	return status, err
}

func (r *StatusRepository) DeleteStatus(tx *pg.Tx, id int) error {
	status := &models.Status{ID: id}
	_, err := tx.Model(status).WherePK().Delete()
	return err
}

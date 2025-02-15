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

func (r *StatusRepository) Create(status *models.Status) error {
	_, err := r.DB.Model(status).Insert()
	return err
}

func (r *StatusRepository) GetAllStatuses() ([]*models.Status, error) {
	statuses := make([]*models.Status, 0)
	err := r.DB.Model(&statuses).Select()
	return statuses, err
}

func (r *StatusRepository) GetStatusById(id int) (*models.Status, error) {
	status := new(models.Status)
	err := r.DB.Model(status).Where("id = ?", id).Select()
	return status, err
}

func (r *StatusRepository) ChangeStatusTitle(id int, title string) (*models.Status, error) {
	status := new(models.Status)
	_, err := r.DB.Model(status).Set("title = ?", title).Where("id = ?", id).Update()
	return status, err
}

func (r *StatusRepository) ChangeStatusDescription(id int, description string) (*models.Status, error) {
	status := new(models.Status)
	_, err := r.DB.Model(status).Set("description = ?", description).Where("id = ?", id).Update()
	return status, err
}

func (r *StatusRepository) DeleteStatus(id int) error {
	status := &models.Status{ID: id}
	_, err := r.DB.Model(status).WherePK().Delete()
	return err
}

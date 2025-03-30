package service

import (
	"event_service/internal/models"
	"event_service/internal/repositories"
	"event_service/internal/schemas"
	"github.com/go-pg/pg/v10"
)

type LocationService struct {
	repo *repositories.LocationRepository
	db   *pg.DB
}

func NewLocationService(repo *repositories.LocationRepository, db *pg.DB) *LocationService {
	return &LocationService{
		repo: repo,
		db:   db,
	}
}

func (s *LocationService) GetAllLocations() (_ []*models.Location, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		err = tx.Commit()
	}()

	return s.repo.GetAllLocations(tx)
}

func (s *LocationService) GetLocationById(locationId int) (_ *models.Location, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}
	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		err = tx.Commit()
	}()

	return s.repo.GetLocationById(tx, locationId)
}

func (s *LocationService) CreateLocation(event schemas.Location) (_ *models.Location, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	model := &models.Location{
		Title: event.Title,
	}

	return s.repo.Create(tx, model)
}

func (s *LocationService) UpdateLocation(locationId int, newLocation schemas.LocationUpdate) (_ *models.Location, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	location, err := s.GetLocationById(locationId)
	if err != nil {
		return nil, err
	}

	if newLocation.Title != "" {
		location.Title = newLocation.Title
	}

	return s.repo.Update(tx, locationId, location)
}

func (s *LocationService) DeleteLocation(locationId int) (err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	return s.repo.DeleteLocation(tx, locationId)
}

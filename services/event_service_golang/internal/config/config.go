package config

import (
	"github.com/ilyakaznacheev/cleanenv"
	"log"
	"os"
	"time"
)

type Config struct {
	Env         string `yaml:"env" env-default:"local"`
	HTTPServer  `yaml:"http_server"`
	SQLDatabase `yaml:"sql_database"`
}

type HTTPServer struct {
	Address     string        `yaml:"address" env-default:"localhost:8081"`
	Timeout     time.Duration `yaml:"timeout" env-default:"10s"`
	IdleTimeout time.Duration `yaml:"idle_timeout" env-default:"60s"`
}

type SQLDatabase struct {
	Addr        string `yaml:"addr" env-default:"postgres:5432"`
	User        string `yaml:"user" env-default:"admin"`
	Password    string `yaml:"password" env-default:"admin"`
	Database    string `yaml:"database" env-default:"postgres"`
	Echo        bool   `yaml:"echo" env-default:"false"`
	EchoPool    bool   `yaml:"echo_pool" env-default:"false"`
	PoolSize    int    `yaml:"pool_size" env-default:"50"`
	MaxOverflow int    `yaml:"max_overflow" env-default:"10"`
}

func MustLoad() *Config {
	configPath := os.Getenv("CONFIG_PATH")
	if configPath == "" {
		log.Fatal("CONFIG_PATH is not set")
	}

	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		log.Fatalf("config file does not exist: %s", configPath)
	}

	var cfg Config
	if err := cleanenv.ReadConfig(configPath, &cfg); err != nil {
		log.Fatalf("cannot read config file: %s", err)
	}

	return &cfg
}

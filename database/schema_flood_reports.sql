-- Tabel untuk menyimpan laporan banjir dengan format Google Sheets
CREATE TABLE IF NOT EXISTS flood_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Timestamp" TEXT,                  -- A: Timestamp (Format: YYYY-MM-DD HH:MM:SS WIB)
    "Alamat" TEXT NOT NULL,            -- B: Alamat
    "Tinggi Banjir" TEXT NOT NULL,     -- C: Tinggi Banjir
    "Nama Pelapor" TEXT NOT NULL,      -- D: Nama Pelapor
    "No HP" TEXT,                      -- E: No HP
    "IP Address" TEXT,                 -- F: IP Address
    "Photo URL" TEXT,                  -- G: Photo URL
    "Status" TEXT DEFAULT 'pending',   -- H: Status
    report_date DATE,                  -- Untuk query berdasarkan tanggal
    report_time TIME,                  -- Untuk query berdasarkan waktu
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index untuk optimasi query
CREATE INDEX IF NOT EXISTS idx_report_date ON flood_reports(report_date);
CREATE INDEX IF NOT EXISTS idx_report_time ON flood_reports(report_time);
CREATE INDEX IF NOT EXISTS idx_ip_address ON flood_reports("IP Address");
CREATE INDEX IF NOT EXISTS idx_status ON flood_reports("Status");

-- Insert sample data (opsional)
INSERT OR IGNORE INTO flood_reports 
("Timestamp", "Alamat", "Tinggi Banjir", "Nama Pelapor", "No HP", "IP Address", "Photo URL", "Status", report_date, report_time)
VALUES 
('2024-01-15 14:30:00', 'Jl. Merdeka No. 12', 'Setinggi lutut', 'Budi Santoso', '08123456789', '192.168.1.100', 'uploads/sample1.jpg', 'pending', '2024-01-15', '14:30:00'),
('2024-01-15 15:45:00', 'Jl. Sudirman No. 45', 'Setinggi betis', 'Ani Wijaya', '08129876543', '192.168.1.101', 'uploads/sample2.jpg', 'verified', '2024-01-15', '15:45:00');
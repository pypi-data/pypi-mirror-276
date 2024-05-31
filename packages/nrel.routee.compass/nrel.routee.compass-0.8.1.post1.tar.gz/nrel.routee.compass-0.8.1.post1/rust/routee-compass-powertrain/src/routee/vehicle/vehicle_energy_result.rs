use routee_compass_core::model::unit::{Energy, EnergyUnit};

use super::VehicleState;

pub struct VehicleEnergyResult {
    pub energy: Energy,
    pub energy_unit: EnergyUnit,
    pub updated_state: VehicleState,
}

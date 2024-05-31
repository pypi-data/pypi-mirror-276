use std::sync::Arc;

use super::edge_rtree_input_plugin::EdgeRtreeInputPlugin;
use crate::{
    app::compass::config::{
        builders::InputPluginBuilder, compass_configuration_error::CompassConfigurationError,
        config_json_extension::ConfigJsonExtensions,
        frontier_model::road_class::road_class_parser::RoadClassParser,
    },
    plugin::input::input_plugin::InputPlugin,
};
use routee_compass_core::model::unit::{Distance, DistanceUnit};

pub struct EdgeRtreeInputPluginBuilder {}

impl InputPluginBuilder for EdgeRtreeInputPluginBuilder {
    fn build(
        &self,
        parameters: &serde_json::Value,
    ) -> Result<Arc<dyn InputPlugin>, CompassConfigurationError> {
        let parent_key = String::from("edge_rtree");
        let linestring_file = parameters.get_config_string(&"geometry_input_file", &parent_key)?;
        let road_class_file = parameters.get_config_string_optional(&"road_class_input_file")?;
        let vehicle_restriction_file =
            parameters.get_config_string_optional(&"vehicle_restriction_input_file")?;

        let distance_tolerance_option =
            parameters.get_config_serde_optional::<Distance>(&"distance_tolerance", &parent_key)?;
        let distance_unit_option =
            parameters.get_config_serde_optional::<DistanceUnit>(&"distance_unit", &parent_key)?;

        let road_class_parser = parameters
            .get_config_serde_optional::<RoadClassParser>(
                &"road_class_parser",
                &"RoadClassFrontierModel",
            )?
            .unwrap_or_default();

        let plugin = EdgeRtreeInputPlugin::new(
            road_class_file,
            vehicle_restriction_file,
            linestring_file,
            distance_tolerance_option,
            distance_unit_option,
            road_class_parser,
        )?;
        Ok(Arc::new(plugin))
    }
}

use crate::{CalculatorCommand, CalculatorManager, GameCalculatorCommand};
use unity::{
    il2cpp,
    prelude::*,
    system::Il2CppString,
};

const COMMAND: &str = "OverlayActive";
const TEMPLATE: &str = "地形回避";

#[unity::class("App", "Unit")]
struct Unit {}

#[unity::class("App", "BattleInfoSide")]
struct BattleInfoSide {}

pub fn register(manager: &mut CalculatorManager) -> bool {
    let command_name: &Il2CppString = COMMAND.into();
    if unsafe { find_command(manager, command_name, None) }.is_some() {
        return true;
    }

    let template_name: &Il2CppString = TEMPLATE.into();
    let Some(template) = (unsafe { find_command(manager, template_name, None) }) else {
        return false;
    };
    let Ok(command) = il2cpp::instantiate_class::<GameCalculatorCommand>(
        template.get_class().clone(),
    ) else {
        return false;
    };

    {
        let class = command.get_class_mut();
        let Some(name_method) = class.get_virtual_method_mut("get_Name") else {
            return false;
        };
        name_method.method_ptr = command_name_impl as *mut u8;

        let Some(unit_method) = class.get_virtual_method_mut("GetImpl") else {
            return false;
        };
        unit_method.method_ptr = get_for_unit as *mut u8;

        // BattleInfoSide overload, verified for Engage 2.0.0.
        let Some(battle_method) = class.get_vtable_mut().get_mut(31) else {
            return false;
        };
        battle_method.method_ptr = get_for_battle as *mut u8;
    }

    unsafe { add_command(manager, command, None) };
    true
}

fn command_name_impl(
    _command: &GameCalculatorCommand,
    _method: OptionalMethod,
) -> &'static Il2CppString {
    COMMAND.into()
}

fn get_for_unit(
    _command: &GameCalculatorCommand,
    unit: *const Unit,
    _method: OptionalMethod,
) -> f32 {
    unsafe { is_on_overlap(unit) as u8 as f32 }
}

fn get_for_battle(
    _command: &GameCalculatorCommand,
    side: &BattleInfoSide,
    _method: OptionalMethod,
) -> f32 {
    let unit = unsafe { battle_side_unit(side, None) };
    unsafe { is_on_overlap(unit) as u8 as f32 }
}

unsafe fn is_on_overlap(unit: *const Unit) -> bool {
    if unit.is_null() || map_terrain(None).is_null() {
        return false;
    }

    let x = unit_x(unit, None);
    let z = unit_z(unit, None);

    // MapOverlap uses the game's fixed 32x32 tile grid.
    if !(0..32).contains(&x) || !(0..32).contains(&z) {
        return false;
    }
    !overlap_terrain(x, z, None).is_null()
}

#[skyline::from_offset(0x0298DAA0)]
fn find_command(
    manager: &CalculatorManager,
    name: &Il2CppString,
    method: OptionalMethod,
) -> Option<&'static mut CalculatorCommand>;

#[skyline::from_offset(0x0298D900)]
fn add_command(
    manager: &mut CalculatorManager,
    command: &GameCalculatorCommand,
    method: OptionalMethod,
) -> *mut CalculatorCommand;

#[skyline::from_offset(0x01F42A60)]
fn map_terrain(method: OptionalMethod) -> *const u8;

#[skyline::from_offset(0x01A54C20)]
fn unit_x(unit: *const Unit, method: OptionalMethod) -> i32;

#[skyline::from_offset(0x01A54C30)]
fn unit_z(unit: *const Unit, method: OptionalMethod) -> i32;

#[skyline::from_offset(0x01DFDA90)]
fn overlap_terrain(x: i32, z: i32, method: OptionalMethod) -> *const u8;

#[skyline::from_offset(0x01E8B250)]
fn battle_side_unit(side: &BattleInfoSide, method: OptionalMethod) -> *const Unit;

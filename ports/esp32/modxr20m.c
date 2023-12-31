#include "py/obj.h"
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/objtuple.h"
#include <stdbool.h>
#include "xr20m_drv.h"

#define MAGIC_CONSTANT 42
STATIC const MP_DEFINE_STR_OBJ(version_string_obj, "1.2.3");

const mp_rom_obj_tuple_t version_tuple_obj = {
    {&mp_type_tuple},
    2,
    {
        MP_ROM_INT(1),
        MP_ROM_PTR(&version_string_obj),
    },
};

STATIC mp_obj_t xr20m_init(void) {
    bool rc = true;
    init_serial();
    // Calculate the addition and convert to MicroPython object.
    return mp_obj_new_bool(rc);
}
// Define a Python reference to the function above.
STATIC MP_DEFINE_CONST_FUN_OBJ_0(xr20m_init_obj, xr20m_init);

STATIC const mp_rom_map_elem_t xr20m_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_xr20m) },
    { MP_ROM_QSTR(MP_QSTR_magic), MP_ROM_INT(MAGIC_CONSTANT) },
    { MP_ROM_QSTR(MP_QSTR_version_tuple), MP_ROM_PTR(&version_tuple_obj) },
    { MP_ROM_QSTR(MP_QSTR_xr20m_init), MP_ROM_PTR(&xr20m_init_obj) },
};
STATIC MP_DEFINE_CONST_DICT(xr20m_module_globals, xr20m_module_globals_table);

const mp_obj_module_t xr20m_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&xr20m_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_xr20m, xr20m_user_cmodule);
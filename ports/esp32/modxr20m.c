#include "py/obj.h"
#include "py/runtime.h"
#include "py/objstr.h"
#include "py/objtuple.h"
#include <stdbool.h>
#include "xr20m_drv.h"

STATIC mp_obj_t xr20m_init(void) {
    bool rc = true;
    init_serial();
    // Calculate the addition and convert to MicroPython object.
    return mp_obj_new_bool(rc);
}
// Define a Python reference to the function above.
STATIC MP_DEFINE_CONST_FUN_OBJ_0(xr20m_init_obj, xr20m_init);

STATIC mp_obj_t xr20m_write(mp_obj_t a_obj, mp_obj_t b_obj) {
    bool rc = true;
    // Extract the ints from the micropython input objects.
    uint8_t ch = mp_obj_get_int(a_obj);
    uint8_t data = mp_obj_get_int(b_obj);
    xr20m_write_ll(ch, data);
    // Calculate the addition and convert to MicroPython object.
    return mp_obj_new_bool(rc);
}
// Define a Python reference to the function above.
STATIC MP_DEFINE_CONST_FUN_OBJ_2(xr20m_write_obj, xr20m_write);

STATIC mp_obj_t xr20m_any(mp_obj_t a_obj) {
    // Extract the ints from the micropython input objects.
    uint8_t ch = mp_obj_get_int(a_obj);
    int bytes_waiting = xr20m_any_ll(ch);
    // Calculate the addition and convert to MicroPython object.
    return mp_obj_new_int(bytes_waiting);
}
// Define a Python reference to the function above.
STATIC MP_DEFINE_CONST_FUN_OBJ_1(xr20m_any_obj, xr20m_any);

STATIC mp_obj_t xr20m_pop(mp_obj_t a_obj) {
    // Extract the ints from the micropython input objects.
    uint8_t ch = mp_obj_get_int(a_obj);
    int bytes_waiting = xr20m_pop_ll(ch);
    // Calculate the addition and convert to MicroPython object.
    return mp_obj_new_int(bytes_waiting);
}
// Define a Python reference to the function above.
STATIC MP_DEFINE_CONST_FUN_OBJ_1(xr20m_pop_obj, xr20m_pop);

STATIC mp_obj_t xr20m_set_baud(mp_obj_t a_obj, mp_obj_t b_obj) {
    bool rc = true;
    // Extract the ints from the micropython input objects.
    uint8_t ch = mp_obj_get_int(a_obj);
    int baud   = mp_obj_get_int(b_obj);
    xr20m_set_baud_ll(ch, baud);
    // Calculate the addition and convert to MicroPython object.
    return mp_obj_new_bool(rc);
}
// Define a Python reference to the function above.
STATIC MP_DEFINE_CONST_FUN_OBJ_2(xr20m_set_baud_obj, xr20m_set_baud);

STATIC mp_obj_t xr20m_set_line(mp_obj_t a_obj, mp_obj_t b_obj, mp_obj_t c_obj) {
    bool rc = true;
    // Extract the ints from the micropython input objects.
    uint8_t ch = mp_obj_get_int(a_obj);
    uint8_t parity   = mp_obj_get_int(b_obj);
    uint8_t stop_bits   = mp_obj_get_int(c_obj);
    xr20m_set_line_ll(ch, parity, stop_bits);
    // Calculate the addition and convert to MicroPython object.
    return mp_obj_new_bool(rc);
}
// Define a Python reference to the function above.
STATIC MP_DEFINE_CONST_FUN_OBJ_3(xr20m_set_line_obj, xr20m_set_line);

STATIC const mp_rom_map_elem_t xr20m_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_xr20m) },
    { MP_ROM_QSTR(MP_QSTR_xr20m_init), MP_ROM_PTR(&xr20m_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_xr20m_write), MP_ROM_PTR(&xr20m_write_obj) },
    { MP_ROM_QSTR(MP_QSTR_xr20m_any), MP_ROM_PTR(&xr20m_any_obj) },
    { MP_ROM_QSTR(MP_QSTR_xr20m_pop), MP_ROM_PTR(&xr20m_pop_obj) },
    { MP_ROM_QSTR(MP_QSTR_xr20m_set_baud), MP_ROM_PTR(&xr20m_set_baud_obj) },
    { MP_ROM_QSTR(MP_QSTR_xr20m_set_line), MP_ROM_PTR(&xr20m_set_line_obj) },
};
STATIC MP_DEFINE_CONST_DICT(xr20m_module_globals, xr20m_module_globals_table);

const mp_obj_module_t xr20m_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&xr20m_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_xr20m, xr20m_user_cmodule);
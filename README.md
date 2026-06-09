# HOUDINI_AUTOMATION_TOOLS
### teo_nemac · Technical Artist Pipeline Scripts

> Python automation tools for Houdini — built to remove repetitive setup work and let artists focus on simulation and look development.

---

## Scripts

### `flipsrc_setup.py` — FLIP Source Setup Tool
Builds a production-ready FLIP simulation network from scratch with a single run.

**What it creates:**

```
/obj
└── flip_sim (geo)
    ├── INSERT_SRC_HERE     (null — plug your source geometry here)
    ├── attr_noise          (attribnoise — displaces P for organic sourcing)
    ├── flip_source         (flipsource — jitter seed driven by $FF)
    ├── speed_noise         (attribwrangle — curl noise velocity setup)
    ├── INSERT_COLL_HERE    (null — plug your collision geometry here)
    └── flip_sim (dopnet)
        ├── flip_object     (flipobject — particle sep configurable)
        ├── volume_source   (volumesource)
        ├── flip_solver     (flipsolver — limit size configurable)
        ├── gravity
        ├── merge
        ├── INSERT_COLL_GEO_HERE (staticobject)
        └── output
```

**UI dialog — configurable at run time:**

| Parameter | Default | Description |
|---|---|---|
| Container Name | `flip_sim` | Name of the top-level geo node |
| Particle Separation | `0.05` | Controls FLIP particle density |
| Limit Size X/Y/Z | `5 / 5 / 5` | FLIP solver domain limit |

**How to use:**
1. Open Houdini → Windows → Python Source Editor
2. Paste or load `flipsrc_setup.py`
3. Run — a dialog will appear to configure the setup
4. Plug your source geo into `INSERT_SRC_HERE` and your collision geo into `INSERT_COLL_HERE` / `INSERT_COLL_GEO_HERE`

---

### `basic_flip_setup_tool.py` — Basic FLIP Setup Tool
A lightweight FLIP setup for quick iteration and look development.

---

## Structure

```
HOUDINI_AUTOMATION_TOOLS/
└── scripts/
    └── python/
        ├── flipsrc_setup.py
        └── basic_flip_setup_tool.py
```

---

## Stack

![Houdini](https://img.shields.io/badge/Houdini-20.5-orange?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

- **Houdini** 20.5+
- **Python** 3.x (via Houdini's embedded interpreter)
- No external dependencies

---

## Author

**Jonathan Escalera** · Technical Artist · Founder  
[teonemac](https://github.com/teonemac) · Querétaro, MX

---

*teo_nemac · Ingeniería Creativa · 2026*

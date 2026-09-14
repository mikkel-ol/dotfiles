return {
  "nvim-tree/nvim-web-devicons",
  opts = {
    strict = true,
    override_by_extension = {
      ["component.ts"] = {
        icon = "",
        color = "#0288d1",
        name = "AngularComponent",
      },
      ["module.ts"] = {
        icon = "",
        color = "#e53835",
        name = "AngularModule",
      },
      ["service.ts"] = {
        icon = "",
        color = "#ffc928",
        name = "AngularService",
      },
      ["routes.ts"] = {
        icon = "󰑪",
        color = "#43a047",
        name = "Routes",
      },
    },
  },
}

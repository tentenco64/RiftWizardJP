# Rift-Wizard 日本語化MOD
Universal API MODを使ってRift Wizardを日本語化します。
元となったUniversal APIとは互換性を保証しないので注意してください。

**導入方法**
Rift Wizardのインストール先\RiftWizard\mods\API_Universal\本MOD
となるようにディレクトリに配置してください。
API_Universalファイルが無い場合は作成してください。


# Rift-Wizard-Universal-API README
## Rift-Wizard-Universal-API
An API meant to improve mods' compatibility by being the only API to override the original source's class methods

**API_Universal, aka Modred**
- combines lots of APIs into one mod.
    - API_Boss
    - API_Disrupt
    - API_Effect
    - API_Music
    - API_OptionsMenu
    - API_Spells
    - API_TitleMenus
    - API_Translations

- Modders: Please use this from now on instead of the individual APIs. We're starting to run into mod conflicts.
- To use API_Universal, `import mods.API_Universal.Modred as Modred`. Check out Modred.py for documentation on all the API functions available.

**requires**
None

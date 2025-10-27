pub mod pilot;
pub mod basic;
pub mod logo;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Language {
    Pilot,
    Basic,
    Logo,
    Python,
    JavaScript,
    Perl,
}

impl Language {
    pub fn from_extension(ext: &str) -> Self {
        match ext.to_lowercase().as_str() {
            "pilot" | "pil" => Language::Pilot,
            "bas" | "basic" => Language::Basic,
            "logo" | "lgo" => Language::Logo,
            "py" | "python" => Language::Python,
            "js" | "javascript" => Language::JavaScript,
            "pl" | "perl" => Language::Perl,
            _ => Language::Pilot,
        }
    }
    
    pub fn name(&self) -> &str {
        match self {
            Language::Pilot => "PILOT",
            Language::Basic => "BASIC",
            Language::Logo => "Logo",
            Language::Python => "Python",
            Language::JavaScript => "JavaScript",
            Language::Perl => "Perl",
        }
    }
}

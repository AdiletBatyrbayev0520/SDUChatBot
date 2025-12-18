package kz.sdu.chat.mainservice.config.internalization;

public enum Language {
    KZ, RU, TR, DE, CN, ES, FR, US;

    public static Language getLanguage(String language) {
        return switch (language.toUpperCase()) {
            case "KZ" -> KZ;
            case "RU" -> RU;
            case "TR" -> TR;
            case "DE" -> DE;
            case "CN" -> CN;
            case "ES" -> ES;
            case "FR" -> FR;
            case "US" -> US;
            default -> {
                System.out.println("Unsupported language: " + language);
                yield US; // Default to US if unsupported
            }
        };
    }
}

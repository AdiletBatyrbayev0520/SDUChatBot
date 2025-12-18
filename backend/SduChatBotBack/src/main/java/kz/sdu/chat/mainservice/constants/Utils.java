package kz.sdu.chat.mainservice.constants;

import kz.sdu.chat.mainservice.config.internalization.Language;
import kz.sdu.chat.mainservice.entities.Role;
import kz.sdu.chat.mainservice.entities.User;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class Utils {
    public static User getCurrentUser() {
        final Authentication authentication = SecurityContextHolder.getContext().getAuthentication();

        if (authentication == null || !authentication.isAuthenticated() || authentication.getPrincipal().equals("anonymousUser"))
            return null;

        return (User) authentication.getPrincipal();
    }

    public static boolean isAdmin() {
        User user = getCurrentUser();

        return user != null && user.getRole() == Role.ADMIN;
    }

    public static Language getCurrentLanguage() {
        var locale = LocaleContextHolder.getLocale();

        return Language.getLanguage(locale.getLanguage());
    }

    /**
     * Преобразует строку userAgent в красивый формат.
     * Например:
     * "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
     * -> "Chrome 132 on Windows 10 (64-bit)"
     * <p>
     * "SM-A217F / 31 MOBILE APPLICATION"
     * -> "Mobile SM-A217F (Android 31)"
     */
    public static String prettifyUserAgent(String userAgent) {
        if (isMobileUserAgent(userAgent)) {
            return prettifyMobileUserAgent(userAgent);
        }
        String os = parseOS(userAgent);
        String browser = parseBrowser(userAgent);
        return browser + " on " + os;
    }

    /**
     * Определяет, является ли userAgent мобильным.
     */
    public static boolean isMobileUserAgent(String userAgent) {
        return userAgent != null && userAgent.toUpperCase().contains("MOBILE APPLICATION");
    }

    /**
     * Преобразует mobile userAgent в красивый формат.
     * Ожидается, что формат: "SM-A217F / 31 MOBILE APPLICATION"
     * Результат: "Mobile SM-A217F (Android 31)"
     */
    private static String prettifyMobileUserAgent(String userAgent) {
        // Ищем шаблон: <device_model> / <android_version>
        Pattern mobilePattern = Pattern.compile("^(\\S+)\\s*/\\s*(\\d+)");
        Matcher matcher = mobilePattern.matcher(userAgent);
        if (matcher.find()) {
            String model = matcher.group(1);
            String androidVersion = matcher.group(2);
            return "Mobile " + model + " (Android " + androidVersion + ")";
        }
        return "Mobile Unknown Device";
    }

    private static String parseOS(String userAgent) {
        Pattern osPattern = Pattern.compile("Windows NT (\\d+\\.\\d+)(;\\s*(Win64; x64))?");
        Matcher osMatcher = osPattern.matcher(userAgent);
        if (osMatcher.find()) {
            String version = osMatcher.group(1);
            String osName = "Windows " + version.split("\\.")[0];
            if (osMatcher.group(3) != null) {
                osName += " (64-bit)";
            }
            return osName;
        }
        return "Unknown OS";
    }

    private static String parseBrowser(String userAgent) {
        // Пример для Chrome
        Pattern chromePattern = Pattern.compile("Chrome/([\\d.]+)");
        Matcher chromeMatcher = chromePattern.matcher(userAgent);
        if (chromeMatcher.find()) {
            String version = chromeMatcher.group(1);
            return "Chrome " + version.split("\\.")[0];
        }
        return "Unknown Browser";
    }
}

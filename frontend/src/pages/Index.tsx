import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { ArticleAnalyzer } from "@/components/ArticleAnalyzer";

const Index = () => {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <ArticleAnalyzer />
      </main>
      <Footer />
    </div>
  );
};

export default Index;

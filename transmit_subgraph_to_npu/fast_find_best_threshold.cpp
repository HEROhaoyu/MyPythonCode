#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>

struct Edge {
    int src;
    int dest;

    Edge(int s, int d) : src(s), dest(d) {}
};

std::vector<Edge> readGraphData(const std::string& filePath) {
    std::vector<Edge> edges;
    std::ifstream file(filePath);

    if (file.is_open()) {
        std::string line;

        while (std::getline(file, line)) {
            std::istringstream iss(line);
            int src, dest;
            iss >> src >> dest;
            edges.emplace_back(src, dest);
        }

        file.close();
    }

    return edges;
}

std::unordered_map<int, int> computeDegrees(const std::vector<Edge>& edges) {
    std::unordered_map<int, int> degrees;

    for (const Edge& edge : edges) {
        degrees[edge.src]++;
        degrees[edge.dest]++;
    }

    return degrees;
}

std::tuple<double, double, int, int> findBestThreshold(const std::vector<std::pair<int, int>>& sortedDegrees,
                                                      const std::vector<Edge>& edges,
                                                      const std::unordered_map<int, int>& degrees,
                                                      int numSamples = 1000,
                                                      double coarseRatio = 0.1,
                                                      double mediumRatio = 0.01,
                                                      double fineRatio = 0.001) {
    double bestFineThreshold = 0.0;
    double maxFineAvgDegree = 0.0;
    int denseEdgesCount = 0;
    int denseVertexSet = 0;

    int maxDegree = sortedDegrees[0].second;
    double coarseThresholdRange = coarseRatio * maxDegree;
    std::unordered_set<int> coarseThresholds;

    for (double threshold = 0; threshold < maxDegree; threshold += coarseThresholdRange) {
        coarseThresholds.insert(static_cast<int>(threshold));
    }

    double bestCoarseThreshold = 0.0;
    double maxCoarseAvgDegree = 0.0;

    for (int threshold : coarseThresholds) {
        int edgeCount = 0;
        std::unordered_set<int> vertexSet;

        for (const Edge& edge : edges) {
            if (degrees.at(edge.src) > threshold && degrees.at(edge.dest) > threshold) {
                vertexSet.insert(edge.src);
                vertexSet.insert(edge.dest);
                edgeCount++;
            }
        }

        if (!vertexSet.empty()) {
            double avgDegree = static_cast<double>(edgeCount) / vertexSet.size();
            if (avgDegree > maxCoarseAvgDegree) {
                maxCoarseAvgDegree = avgDegree;
                bestCoarseThreshold = threshold;
            }
        }
    }

    double mediumThresholdRange = mediumRatio * coarseThresholdRange;
    std::vector<double> mediumThresholds;

    for (double threshold = bestCoarseThreshold - mediumThresholdRange;
         threshold < bestCoarseThreshold + mediumThresholdRange;
         threshold += mediumThresholdRange) {
        mediumThresholds.push_back(threshold);
    }

    double bestMediumThreshold = 0.0;
    double maxMediumAvgDegree = 0.0;

    for (double threshold : mediumThresholds) {
        int edgeCount = 0;
        std::unordered_set<int> vertexSet;

        for (const Edge& edge : edges) {
            if (degrees.at(edge.src) > threshold && degrees.at(edge.dest) > threshold) {
                vertexSet.insert(edge.src);
                vertexSet.insert(edge.dest);
                edgeCount++;
            }
        }

        if (!vertexSet.empty()) {
            double avgDegree = static_cast<double>(edgeCount) / vertexSet.size();
            if (avgDegree > maxMediumAvgDegree) {
                maxMediumAvgDegree = avgDegree;
                bestMediumThreshold = threshold;
            }
        }
    }

    double fineThresholdRange = fineRatio * mediumThresholdRange;
    std::vector<double> fineThresholds;

    for (double threshold = bestMediumThreshold - fineThresholdRange;
         threshold < bestMediumThreshold + fineThresholdRange;
         threshold += fineThresholdRange) {
        fineThresholds.push_back(threshold);
    }

    for (double threshold : fineThresholds) {
        int edgeCount = 0;
        std::unordered_set<int> vertexSet;

        for (const Edge& edge : edges) {
            if (degrees.at(edge.src) > threshold && degrees.at(edge.dest) > threshold) {
                vertexSet.insert(edge.src);
                vertexSet.insert(edge.dest);
                edgeCount++;
            }
        }

        if (!vertexSet.empty()) {
            double avgDegree = static_cast<double>(edgeCount) / vertexSet.size();
            if (avgDegree > maxFineAvgDegree) {
                maxFineAvgDegree = avgDegree;
                bestFineThreshold = threshold;
                denseEdgesCount = edgeCount;
                denseVertexSet = vertexSet.size();
            }
        }
    }

    return std::make_tuple(bestFineThreshold, maxFineAvgDegree, denseEdgesCount, denseVertexSet);
}

int main() {
    std::string inputPath = "C:\\Users\\huao\\Desktop\\MyPythonCode\\dataset\\Social networks\\Wiki-Vote.txt";
    std::vector<Edge> edges = readGraphData(inputPath);
    std::string datasetName = "Social Network";
    int numSamples = 1000;

    std::unordered_map<int, int> degrees = computeDegrees(edges);
    std::vector<std::pair<int, int>> sortedDegrees(degrees.begin(), degrees.end());
    std::sort(sortedDegrees.begin(), sortedDegrees.end(),
              [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
                  return a.second > b.second;
              });

    double bestFineThreshold, maxFineAvgDegree;
    int denseEdgesCount, denseVertexSet;

    std::tie(bestFineThreshold, maxFineAvgDegree, denseEdgesCount, denseVertexSet) =
        findBestThreshold(sortedDegrees, edges, degrees);

    std::cout << "Dataset Name: " << datasetName << std::endl;
    std::cout << "Best Threshold: " << bestFineThreshold << std::endl;
    std::cout << "Best Threshold's Avg. Degree: " << maxFineAvgDegree << std::endl;
    std::cout << "Dense Edges Count: " << denseEdgesCount << std::endl;
    std::cout << "Dense Vertex Set: " << denseVertexSet << std::endl;

    return 0;
}
